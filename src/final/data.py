"""Load per-cell feature tables of the three datasets and turn them into (dataframe, label vector) for the final models.

All paths are relative to --data-root (Colab: /content/drive/MyDrive/Project-Skripsi). Feature tables are produced by
the extraction steps in notebooks/colab/final_ml_colab.ipynb and stored in Drive data/processed/.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from skimage.filters import threshold_otsu

ESSIG_LIVE, ESSIG_DEAD = ["T_cell", "T_cell_with_signaling"], ["Dead_Cell"]


def _stain(df):
    return np.log1p(np.clip(pd.to_numeric(df["Live-Dead_mean"], errors="coerce").to_numpy(float), 0, None))


def load_essig(root: Path, cfg: dict):
    """Model A. Expert labels where an experiment has >= min_expert of both classes, else Live-Dead stain label
    (Otsu threshold on that experiment's random sample). The stain channel is never a model input."""
    d = root / cfg["data"]["features_dir"]
    frames, info = [], {}
    files = sorted(d.glob("exp*_features.csv"))
    if not files:
        raise FileNotFoundError(f"no exp*_features.csv in {d}")
    for f in files:
        df = pd.read_csv(f, keep_default_na=False, low_memory=False)
        exp = str(df.exp.iat[0])
        lab = df[df.expert_label.isin(ESSIG_LIVE + ESSIG_DEAD)].copy()
        rnd = df[df.in_random_sample.astype(str) == "True"].copy()
        thr = float(threshold_otsu(_stain(rnd))) if len(rnd) else np.nan
        n_live, n_dead = int(lab.expert_label.isin(ESSIG_LIVE).sum()), int(lab.expert_label.isin(ESSIG_DEAD).sum())
        e = {"rows": int(len(df)), "expert_live": n_live, "expert_dead": n_dead, "stain_threshold_log1p": round(thr, 3)}
        if min(n_live, n_dead) >= cfg["data"].get("min_expert", 50):
            lab["y"], lab["label_source"] = lab.expert_label.isin(ESSIG_DEAD).astype(int), "ahli"
            use = lab
            s = _stain(lab)
            if np.isfinite(thr):
                from sklearn.metrics import cohen_kappa_score, roc_auc_score
                e["stain_vs_expert_auc"] = round(float(roc_auc_score(lab.y, s)), 3)
                e["stain_vs_expert_kappa"] = round(float(cohen_kappa_score(lab.y, (s > thr).astype(int))), 3)
        else:
            rnd["y"], rnd["label_source"] = (_stain(rnd) > thr).astype(int), "pewarna Live-Dead"
            use = rnd
        e.update(label_source=str(use.label_source.iat[0]), n_used=int(len(use)), n_dead_used=int(use.y.sum()))
        info[exp] = e
        frames.append(use)
    df = pd.concat(frames, ignore_index=True)
    df["donor_id"] = df.exp.astype(str) + "/" + df.donor.astype(str)
    for c in [c for c in df.columns if c.startswith("BF_")]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.reset_index(drop=True), df.y.to_numpy(int), info


def load_heidata(root: Path, cfg: dict):
    """Model B. Mock = not infected (0), HIV-1 exposed (+Vpx / -Vpx) = infected (1); only figures that contain Mock
    and a capsid (CA) channel."""
    df = pd.read_csv(root / cfg["data"]["cells"])
    df = df[df.figure.astype(str).isin([str(f) for f in cfg["data"]["figures"]])]
    df = df[df.condition.isin(cfg["data"]["positive"] + cfg["data"]["negative"])].copy()
    need = sorted({c for fs in cfg["feature_sets"].values() for c in fs})
    df = df.dropna(subset=[c for c in need if c.startswith("ca_")]).reset_index(drop=True)
    y = df.condition.isin(cfg["data"]["positive"]).astype(int).to_numpy()
    info = {"per_figure_condition": {f"{a}/{b}": int(n) for (a, b), n in df.groupby(["figure", "condition"]).size().items()}}
    return df, y, info


def load_illinois(root: Path, cfg: dict):
    """Model C. Control wells of all plates: untreated = latent (0), TNF-alpha = active (1), alsterpaullone = suppressed (2)."""
    df = pd.read_csv(root / cfg["data"]["cells"]).replace([np.inf, -np.inf], np.nan)
    cmap = cfg["data"]["condition_to_class"]
    df = df[df.condition.isin(cmap)].reset_index(drop=True)
    y = df.condition.map(cmap).to_numpy(int)
    info = {"per_plate_condition": {f"{a}/{b}": int(n) for (a, b), n in df.groupby(["plate", "condition"]).size().items()},
            "wells": int(df.well.nunique())}
    return df, y, info


LOADERS = {"essig": load_essig, "heidata": load_heidata, "illinois": load_illinois}


def feature_list(df: pd.DataFrame, spec) -> list:
    """spec = explicit list of columns, or {'prefix': 'BF_'}."""
    if isinstance(spec, dict) and "prefix" in spec:
        return sorted(c for c in df.columns if c.startswith(spec["prefix"]))
    return list(spec)
