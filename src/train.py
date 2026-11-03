"""Training entry point.

Usage:
    python src/train.py --config configs/baseline.yaml

Skeleton only: data loading and model building are not implemented yet
because the dataset and model choice are still undecided (see AGENTS.md).
"""
import argparse
import json
import os
import random
from datetime import datetime
from pathlib import Path

import numpy as np
import yaml


def set_seed(seed: int) -> None:
    """Fix all random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a CD4 cell condition classifier.")
    parser.add_argument("--config", default="configs/baseline.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    set_seed(cfg["seed"])

    run_id = f"{cfg['experiment_name']}-{datetime.now():%Y%m%d-%H%M%S}"
    out_dir = Path(cfg["output"]["results_dir"]) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save the exact config used, so every result is traceable.
    with open(out_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

    # TODO: load dataset from cfg["data"]["dir"] (src/data/)
    # TODO: build model from cfg["model"] (src/models/)
    # TODO: training loop; save checkpoints OUTSIDE the repo (Drive Skripsi-ML/models/)
    raise NotImplementedError(
        "Dataset and model are not defined yet. Fill configs/ and implement src/data, src/models."
    )


if __name__ == "__main__":
    main()
