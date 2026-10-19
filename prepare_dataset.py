"""
SignBridge — Safe Dataset Preparation & Feature Extraction.
Enforces:
- Safe archive extraction (path traversal / Zip Slip protection)
- Storage budget checks (Max 5 GB extracted storage)
- Image import cap (Max 100,000 images)
- Duplicate and corrupt file rejection
- Extraction of 21 3D hand landmarks -> 63 invariant geometric features
- Session-aware train/val/test splitting
"""

import argparse
import glob
import hashlib
import json
import os
import sys
import zipfile
from typing import Any, Dict, List, Optional, Set, Tuple

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import cv2
import numpy as np
import pandas as pd

from config import (
    DATA_DIR,
    EXTRACTED_DATASETS_DIR,
    MANIFEST_PATH,
    MAX_EXTRACTED_STORAGE_BYTES,
    MAX_TRAINING_IMAGES,
    PROCESSED_DATA_PATH,
    RAW_DATASETS_DIR,
    ResourceBudgetTracker,
)
try:
    from backend.data_collection import DatasetManager, ISL_ALPHABET_LETTERS, CORE_ISL_GESTURES
    from backend.hand_tracking import HandTracker
    from backend.preprocessing import LandmarkPreprocessor
except ImportError:
    from src.data_collection import DatasetManager, ISL_ALPHABET_LETTERS, CORE_ISL_GESTURES
    from src.hand_tracking import HandTracker
    from src.preprocessing import LandmarkPreprocessor


def is_safe_zip_path(target_dir: str, member_name: str) -> bool:
    """
    Prevents Zip Slip / Path Traversal attacks by verifying extracted file
    is strictly within the destination directory.
    """
    resolved_target = os.path.abspath(target_dir)
    resolved_member = os.path.abspath(os.path.join(target_dir, member_name))
    return resolved_member.startswith(resolved_target + os.sep) or resolved_member == resolved_target


def safe_extract_archive(
    zip_path: str,
    dest_dir: str,
    tracker: ResourceBudgetTracker,
) -> Tuple[bool, str, int]:
    """
    Extracts a zip archive safely while enforcing storage limits and path safety.
    """
    if not os.path.exists(zip_path):
        return False, f"Archive not found: {zip_path}", 0

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            # 1. Check total uncompressed size before extracting
            total_uncompressed = sum(info.file_size for info in zf.infolist())

            can_ext, reason = tracker.check_can_extract(total_uncompressed)
            if not can_ext:
                return False, f"Storage limit exceeded: {reason}", 0

            # 2. Check for path traversal vulnerabilities in all archive entries
            for info in zf.infolist():
                if not is_safe_zip_path(dest_dir, info.filename):
                    return False, f"Security risk: Archive contains unsafe path traversal member: '{info.filename}'", 0

            # 3. Extract files safely
            os.makedirs(dest_dir, exist_ok=True)
            zf.extractall(dest_dir)

            tracker.record_extraction(os.path.basename(zip_path), total_uncompressed)
            return True, f"Successfully extracted {len(zf.infolist())} entries ({round(total_uncompressed / (1024*1024), 2)} MB).", total_uncompressed

    except Exception as e:
        return False, f"Archive extraction failed: {e}", 0


def compute_file_hash(filepath: str) -> str:
    """Computes SHA-256 hash to detect duplicate images."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_image_files(base_dir: str) -> List[Tuple[str, str]]:
    """
    Recursively scans base_dir for images and attempts to infer the sign label
    from the parent folder name (e.g. .../A/image_01.jpg -> label 'A').
    Returns List of (image_path, label).
    """
    valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    found: List[Tuple[str, str]] = []

    for root, _, files in os.walk(base_dir):
        parent_folder = os.path.basename(root).strip().upper()
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in valid_exts:
                # Infer label: If parent folder is a letter (A-Z) or core gesture, use it
                label = parent_folder
                if len(label) == 1 and label in ISL_ALPHABET_LETTERS:
                    found.append((os.path.join(root, f), label))
                elif label in CORE_ISL_GESTURES:
                    found.append((os.path.join(root, f), label))
                else:
                    # Check if filename itself starts with letter (e.g. A_01.jpg)
                    first_part = f.split("_")[0].upper()
                    if first_part in ISL_ALPHABET_LETTERS or first_part in CORE_ISL_GESTURES:
                        found.append((os.path.join(root, f), first_part))

    return found


def process_images_to_landmarks(
    image_entries: List[Tuple[str, str]],
    dataset_name: str,
    tracker: ResourceBudgetTracker,
    max_images_limit: int = MAX_TRAINING_IMAGES,
) -> Dict[str, Any]:
    """
    Extracts 63 invariant MediaPipe landmarks from images and appends them to isl_dataset.csv.
    Enforces maximum image limit (100,000) and filters duplicates.
    """
    dataset_mgr = DatasetManager(PROCESSED_DATA_PATH)
    hand_tracker = HandTracker(max_num_hands=1)
    preprocessor = LandmarkPreprocessor()

    processed_samples: List[Tuple[str, np.ndarray, str, str, str]] = []
    seen_hashes: Set[str] = set()
    label_counts: Dict[str, int] = {}
    corrupted_count = 0
    duplicate_count = 0
    no_hand_count = 0

    total_to_process = min(len(image_entries), max_images_limit)
    print(f"[*] Processing {total_to_process} images (Budget Limit: {max_images_limit})...")

    can_proc, proc_reason = tracker.check_can_process_images(total_to_process)
    if not can_proc:
        print(f"[BUDGET LIMIT] {proc_reason}")
        return {"error": proc_reason}

    for idx, (img_path, label) in enumerate(image_entries[:total_to_process]):
        # Duplicate detection via hash
        try:
            f_hash = compute_file_hash(img_path)
            if f_hash in seen_hashes:
                duplicate_count += 1
                continue
            seen_hashes.add(f_hash)
        except Exception:
            corrupted_count += 1
            continue

        # Load image via OpenCV
        img = cv2.imread(img_path)
        if img is None:
            corrupted_count += 1
            continue

        # Run MediaPipe hand detection
        detection = hand_tracker.detect(img)
        if not detection.has_hand or not detection.hands:
            no_hand_count += 1
            continue

        features = preprocessor.extract_from_landmarks(detection.hands[0].landmarks)
        if features is None:
            no_hand_count += 1
            continue

        session_id = f"batch_{dataset_name}"
        participant_id = f"ds_{dataset_name[:12]}"
        handedness = detection.hands[0].handedness or "Right"

        processed_samples.append((label, features, session_id, participant_id, handedness))
        label_counts[label] = label_counts.get(label, 0) + 1

        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1}/{total_to_process} images... ({len(processed_samples)} valid landmarks extracted)")

    # Save extracted samples into isl_dataset.csv
    added_count = 0
    if processed_samples:
        added_count = dataset_mgr.append_samples_batch(processed_samples)
        tracker.record_images_processed(total_to_process)

    return {
        "total_images_scanned": total_to_process,
        "valid_landmarks_extracted": added_count,
        "corrupted_images": corrupted_count,
        "duplicates_skipped": duplicate_count,
        "no_hand_detected": no_hand_count,
        "samples_per_label": label_counts,
    }


def main():
    parser = argparse.ArgumentParser(description="SignBridge Safe Dataset Preparation & Landmark Extractor")
    parser.add_argument("--extract-all", action="store_true", help="Safely extract all downloaded zip archives")
    parser.add_argument("--process-images", action="store_true", help="Process extracted images into 63 invariant landmark features")
    parser.add_argument("--max-images", type=int, default=10000, help="Maximum images to process in this run (Hard cap 100,000)")
    args = parser.parse_args()

    tracker = ResourceBudgetTracker()
    summary = tracker.get_summary()

    print("=" * 70)
    print("SignBridge — Safe Dataset Preparation & Feature Extractor")
    print("=" * 70)
    print(f"• Extracted Storage Used: {summary['extracted_mb']} MB / {summary['max_extracted_mb']} MB")
    print(f"• Images Processed:       {summary['images_processed']} / {summary['max_images']}")
    print("=" * 70)

    # 1. Check for raw archives to extract
    raw_archives = glob.glob(os.path.join(RAW_DATASETS_DIR, "*.zip"))
    if args.extract_all or not args.process_images:
        if raw_archives:
            print(f"\n[*] Found {len(raw_archives)} raw archive(s) in '{RAW_DATASETS_DIR}':")
            for arc in raw_archives:
                folder_name = os.path.splitext(os.path.basename(arc))[0]
                dest = os.path.join(EXTRACTED_DATASETS_DIR, folder_name)
                print(f"  Extracting: {os.path.basename(arc)} -> {dest}...")
                success, msg, _ = safe_extract_archive(arc, dest, tracker)
                print(f"  Result: {msg}")
        else:
            print(f"\n[INFO] No raw zip archives found in '{RAW_DATASETS_DIR}'.")
            print("  Use 'python download_datasets.py --download' to obtain datasets within budget.")

    # 2. Check for extracted folders to process
    if args.process_images:
        extracted_dirs = [d for d in glob.glob(os.path.join(EXTRACTED_DATASETS_DIR, "*")) if os.path.isdir(d)]
        if not extracted_dirs:
            print(f"[INFO] No extracted datasets found in '{EXTRACTED_DATASETS_DIR}'.")
            return

        for ds_dir in extracted_dirs:
            ds_name = os.path.basename(ds_dir)
            print(f"\n[*] Scanning '{ds_name}' for labeled sign language images...")
            found_entries = find_image_files(ds_dir)
            print(f"  Found {len(found_entries)} labeled images.")

            if found_entries:
                res = process_images_to_landmarks(
                    found_entries,
                    dataset_name=ds_name,
                    tracker=tracker,
                    max_images_limit=min(args.max_images, MAX_TRAINING_IMAGES),
                )
                print("\nProcessing Results Summary:")
                for k, v in res.items():
                    print(f"  • {k}: {v}")


if __name__ == "__main__":
    main()

