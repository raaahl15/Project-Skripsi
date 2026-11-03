"""Evaluation entry point.

Usage:
    python src/evaluate.py --run results/<run_id>

Metrics are written to results/<run_id>/metrics.json. Numbers in the thesis
must be taken from these files, never typed from memory.
"""
import argparse
import json
from pathlib import Path


def save_metrics(run_dir: Path, metrics: dict) -> Path:
    """Write metrics to results/<run_id>/metrics.json."""
    path = run_dir / "metrics.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained model on the test split.")
    parser.add_argument("--run", required=True, help="Path to results/<run_id>")
    args = parser.parse_args()

    run_dir = Path(args.run)
    if not run_dir.exists():
        raise FileNotFoundError(run_dir)

    # TODO: load model checkpoint and test split
    # TODO: compute metrics listed in config (e.g. sklearn.metrics.classification_report, confusion_matrix)
    # TODO: Grad-CAM visualisations -> run_dir / "gradcam/"
    raise NotImplementedError("Evaluation is not implemented yet.")


if __name__ == "__main__":
    main()
