"""Pilot (feasibility) for scheme 1: pretrain a small CNN on Essig IFC T cells, fine-tune on heiDATA (+Vpx vs -Vpx).

Steps
 1. Essig: 24k cells (2 donors x 4 conditions x 3000), one random fluorescence channel per cell, 64x64.
    Pretraining task = 4-class condition; validated on the held-out donor (sanity check of what the CNN learns).
 2. heiDATA: single-cell crops (17 um box around each segmented nucleus, Lamin B1 max projection -> 64x64).
 3. +Vpx vs -Vpx with leave-one-FIGURE-out: CNN from scratch vs CNN initialized from the Essig weights.
 4. Grad-CAM for the fine-tuned model on held-out cells of one figure.
CPU-only, fixed seeds. Outputs in results/pilot-cnn/.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from skimage.transform import resize
from sklearn.metrics import balanced_accuracy_score, roc_auc_score

from src.data.essig import build_pretrain_set
from src.data.heidata import FIELDS, PIXEL_SIZE_UM, field_id, load_stack, max_projection
from src.models.cnn import SmallCNN, grad_cam

SEED = 42


def set_seed(s: int) -> None:
    np.random.seed(s)
    torch.manual_seed(s)


def augment(x: torch.Tensor) -> torch.Tensor:
    """Random flips + 90-degree rotations (orientation is arbitrary for single cells)."""
    if torch.rand(1) < 0.5:
        x = x.flip(-1)
    if torch.rand(1) < 0.5:
        x = x.flip(-2)
    return torch.rot90(x, int(torch.randint(0, 4, (1,))), dims=(-2, -1))


def train(model, X, y, epochs, lr, batch=64, weight=None):
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    lossf = nn.CrossEntropyLoss(weight=weight)
    Xt, yt = torch.from_numpy(X[:, None]), torch.from_numpy(y).long()
    for _ in range(epochs):
        model.train()
        perm = torch.randperm(len(Xt))
        for i in range(0, len(Xt), batch):
            idx = perm[i:i + batch]
            opt.zero_grad()
            lossf(model(augment(Xt[idx])), yt[idx]).backward()
            opt.step()
    return model


@torch.no_grad()
def predict_proba(model, X, batch=256):
    """Batched inference (predicting ~12k images at once needs ~3 GB RAM and crashed the first pilot run)."""
    model.eval()
    out = [torch.softmax(model(torch.from_numpy(X[i:i + batch, None])), dim=1).numpy()
           for i in range(0, len(X), batch)]
    return np.concatenate(out)


def heidata_crops(root: Path, labels_dir: Path, box_um: float = 17.0) -> pd.DataFrame:
    half = int(round(box_um / PIXEL_SIZE_UM / 2))
    rows = []
    for f in FIELDS:
        fid = field_id(f)
        lab = np.load(labels_dir / f"{fid}.npy")
        lam = max_projection(load_stack(root, f), f.channels["lamin"])
        lo, hi = np.percentile(lam, [1, 99.8])
        lam = np.clip((lam - lo) / max(hi - lo, 1e-6), 0, 1)
        pad = np.pad(lam, half, mode="constant", constant_values=0)
        for k in range(1, lab.max() + 1):
            rr, cc = np.nonzero(lab == k)
            if not len(rr):
                continue
            r, c = int(rr.mean()) + half, int(cc.mean()) + half
            crop = resize(pad[r - half:r + half, c - half:c + half], (64, 64), anti_aliasing=True)
            rows.append({"field": fid, "figure": f.figure, "condition": f.condition, "img": crop.astype(np.float32)})
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--essig-zip", required=True)
    ap.add_argument("--heidata", default="data/raw/heidata-MUXYRY")
    ap.add_argument("--labels", default="results/pilot-heidata/labels")
    ap.add_argument("--out", default="results/pilot-cnn")
    ap.add_argument("--per-group", type=int, default=3000)
    ap.add_argument("--pre-epochs", type=int, default=6)
    ap.add_argument("--ft-epochs", type=int, default=40)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(max(1, torch.get_num_threads()))
    res = {}

    # 1. Essig pretraining (cache the sampled set to data/processed)
    cache = Path("data/processed/essig_pretrain_64.npz")
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists():
        d = dict(np.load(cache))
    else:
        d = build_pretrain_set(Path(args.essig_zip), per_group=args.per_group, seed=SEED)
        np.savez_compressed(cache, **d)
    donors = sorted(set(d["donor"]))
    tr, te = d["donor"] != donors[-1], d["donor"] == donors[-1]
    set_seed(SEED)
    pre = train(SmallCNN(4), d["X"][tr], d["y"][tr], args.pre_epochs, 1e-3, batch=128)
    acc = float((predict_proba(pre, d["X"][te]).argmax(1) == d["y"][te]).mean())
    res["pretrain"] = {"n_train": int(tr.sum()), "n_test_heldout_donor": int(te.sum()),
                       "heldout_donor": donors[-1], "4class_accuracy_heldout_donor": round(acc, 3), "chance": 0.25}
    print("pretrain 4-class acc on held-out donor:", round(acc, 3))
    set_seed(SEED)
    pre = train(pre, d["X"][te], d["y"][te], 1, 5e-4, batch=128)  # brief pass on the other donor too
    torch.save(pre.state_dict(), out / "essig_pretrained.pt")

    # 2-3. heiDATA +Vpx vs -Vpx, leave-one-figure-out
    cells = heidata_crops(Path(args.heidata), Path(args.labels))
    cells = cells[cells.condition.isin(["+Vpx", "-Vpx"])].reset_index(drop=True)
    X = np.stack(cells.img.to_numpy())
    y = (cells.condition == "+Vpx").astype(int).to_numpy()
    figs = cells.figure.to_numpy()
    w = torch.tensor([len(y) / (2 * (y == 0).sum()), len(y) / (2 * (y == 1).sum())], dtype=torch.float32)
    for variant in ["scratch", "pretrained"]:
        proba = np.zeros(len(y))
        for fig_out in sorted(set(figs)):
            set_seed(SEED)
            m = SmallCNN(4)
            if variant == "pretrained":
                m.load_state_dict(torch.load(out / "essig_pretrained.pt"))
            m.replace_head(2)
            lr = 1e-3 if variant == "scratch" else 3e-4
            m = train(m, X[figs != fig_out], y[figs != fig_out], args.ft_epochs, lr, batch=32, weight=w)
            proba[figs == fig_out] = predict_proba(m, X[figs == fig_out])[:, 1]
            if variant == "pretrained" and fig_out == "3B":
                sel = np.where(figs == fig_out)[0][:12]
                cams = grad_cam(m, torch.from_numpy(X[sel][:, None]), target_class=1)
                fig, axes = plt.subplots(2, 12, figsize=(18, 3.4))
                for j, i in enumerate(sel):
                    axes[0, j].imshow(X[i], cmap="gray")
                    axes[0, j].set_title(f"{cells.condition[i]} p={proba[i]:.2f}", fontsize=7)
                    axes[1, j].imshow(X[i], cmap="gray")
                    axes[1, j].imshow(cams[j], cmap="jet", alpha=0.45)
                    axes[0, j].axis("off")
                    axes[1, j].axis("off")
                fig.suptitle("Grad-CAM (class +Vpx), fine-tuned CNN, held-out figure 3B (Lamin B1)", fontsize=9)
                fig.savefig(out / "gradcam_3B.png", dpi=110, bbox_inches="tight")
                plt.close(fig)
        r = {"roc_auc": round(roc_auc_score(y, proba), 3),
             "balanced_accuracy": round(balanced_accuracy_score(y, proba >= 0.5), 3), "n_cells": int(len(y))}
        res[f"heidata_vpx_{variant}"] = r
        print(f"heiDATA +Vpx vs -Vpx, CNN {variant}: {r}")

    (out / "metrics.json").write_text(json.dumps(res, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
