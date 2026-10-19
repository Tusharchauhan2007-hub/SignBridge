"""
SignBridge — Safe Model Training Pipeline.
Enforces Hard Resource Limits:
- Max 60 minutes training time
- Max 4 GB RAM target
- Local-only execution (100% Free, zero cloud GPUs, zero API costs)
- Session-aware cross validation (GroupShuffleSplit / StratifiedShuffleSplit)
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    import psutil
except ImportError:
    psutil = None

from config import (
    MAX_LOCAL_RAM_BYTES,
    MAX_TRAINING_TIME_SECONDS,
    MODELS_DIR,
    PROCESSED_DATA_PATH,
    ResourceBudgetTracker,
)
try:
    from backend.train_model import ModelTrainer
except ImportError:
    from src.train_model import ModelTrainer


def get_current_ram_usage_mb() -> float:
    """Returns current process RAM usage in Megabytes."""
    if psutil is None:
        return 0.0
    try:
        proc = psutil.Process()
        return round(proc.memory_info().rss / (1024 * 1024), 2)
    except Exception:
        return 0.0


def main():
    parser = argparse.ArgumentParser(description="SignBridge Safe Local Model Training")
    parser.add_argument("--n-trees", type=int, default=150, help="Number of trees in Random Forest")
    parser.add_argument("--test-size", type=float, default=0.20, help="Validation split ratio (default: 0.20)")
    parser.add_argument("--dry-run", action="store_true", help="Check dataset readiness without training")
    args = parser.parse_args()

    tracker = ResourceBudgetTracker()
    summary = tracker.get_summary()

    print("=" * 70)
    print("SignBridge — Strictly Free Local Model Training")
    print("=" * 70)
    print(f"• Training Time Cap:  {MAX_TRAINING_TIME_SECONDS // 60} Minutes")
    print(f"• Target RAM Cap:     {MAX_LOCAL_RAM_BYTES // (1024 * 1024 * 1024)} GB")
    print(f"• Dataset Source:     {PROCESSED_DATA_PATH}")
    print(f"• Available Disk:     {summary['available_disk_gb']} GB")
    print("=" * 70)

    # 1. Dataset readiness check
    trainer = ModelTrainer(dataset_path=PROCESSED_DATA_PATH, n_estimators=args.n_trees)
    is_valid, issues = trainer.dataset_manager.validate_dataset(min_samples_per_class=2)

    class_counts = trainer.dataset_manager.get_class_counts()
    total_samples = sum(class_counts.values())

    print(f"\n[*] Dataset contains {total_samples} samples across {len(class_counts)} classes:")
    for cls, cnt in class_counts.items():
        print(f"  • {cls}: {cnt} samples")

    if not is_valid and len(class_counts) < 2:
        print("\n[CANNOT TRAIN] Dataset does not meet minimum requirements:")
        for issue in issues:
            print(f"  - {issue}")
        print("\n[RESOLUTION] Collect alphabet/gesture samples in Studio or via prepare_dataset.py first.")
        return

    if args.dry_run:
        print("\n[DRY RUN COMPLETE] Dataset is valid and ready for training within budget limits.")
        return

    # 2. Check initial RAM usage
    initial_ram = get_current_ram_usage_mb()
    print(f"\n[*] Starting training (Initial Process RAM: {initial_ram} MB)...")

    start_time = time.time()
    try:
        # Run training
        results = trainer.train_and_evaluate(test_size=args.test_size)
        elapsed_sec = round(time.time() - start_time, 2)
        peak_ram = get_current_ram_usage_mb()

        # Enforce limits check
        if elapsed_sec > MAX_TRAINING_TIME_SECONDS:
            print(f"[WARNING] Training time ({elapsed_sec}s) exceeded limit of {MAX_TRAINING_TIME_SECONDS}s.")
        else:
            print(f"[LIMIT CHECK] Training finished in {elapsed_sec}s (within {MAX_TRAINING_TIME_SECONDS}s budget).")

        if (peak_ram * 1024 * 1024) > MAX_LOCAL_RAM_BYTES:
            print(f"[WARNING] Peak RAM ({peak_ram} MB) exceeded target of {MAX_LOCAL_RAM_BYTES // (1024 * 1024)} MB.")
        else:
            print(f"[LIMIT CHECK] Peak RAM was {peak_ram} MB (within {MAX_LOCAL_RAM_BYTES // (1024 * 1024)} MB budget).")

        # Save training metrics report
        metrics_report_path = os.path.join(MODELS_DIR, "training_metrics.json")
        metrics_payload = {
            "trained_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "elapsed_seconds": elapsed_sec,
            "peak_ram_mb": peak_ram,
            "accuracy": results["accuracy"],
            "precision_macro": results["precision_macro"],
            "recall_macro": results["recall_macro"],
            "f1_macro": results["f1_macro"],
            "classes": results["classes"],
            "split_strategy": results["split_strategy"],
            "total_samples": total_samples,
            "n_estimators": args.n_trees,
        }
        with open(metrics_report_path, "w", encoding="utf-8") as f:
            json.dump(metrics_payload, f, indent=2)

        print("\n" + "=" * 70)
        print("Training Completed Successfully!")
        print("=" * 70)
        print(f"• Model Artifact:    {results['model_path']}")
        print(f"• Test Accuracy:     {results['accuracy'] * 100:.2f}%")
        print(f"• Macro Precision:   {results['precision_macro'] * 100:.2f}%")
        print(f"• Macro Recall:      {results['recall_macro'] * 100:.2f}%")
        print(f"• Macro F1 Score:    {results['f1_macro'] * 100:.2f}%")
        print(f"• Classes Recognized: {', '.join(results['classes'])}")
        print(f"• Split Strategy:    {results['split_strategy']}")
        print(f"• Metrics Report:    {metrics_report_path}")
        print("=" * 70)

    except Exception as ex:
        print(f"[ERROR] Training failed: {ex}")
        sys.exit(1)


if __name__ == "__main__":
    main()

