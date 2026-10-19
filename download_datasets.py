"""
SignBridge — Dataset Downloader & Kaggle API Search.
Enforces 100% Free-Only Policy and Hard Budget Caps:
- Max 2 GB download limit
- Max 10 datasets
- Max 100 Kaggle API calls
- Dry-run estimation mode
- Manifest logging with licenses and sources
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import (
    BudgetExceededError,
    DATA_DIR,
    MANIFEST_PATH,
    MAX_DATASETS,
    MAX_DOWNLOAD_RETRIES,
    MAX_KAGGLE_API_REQUESTS,
    MAX_TOTAL_DOWNLOAD_BYTES,
    RAW_DATASETS_DIR,
    ResourceBudgetTracker,
)

# Curated reference catalog of verified, 100% free open-access sign language datasets
CURATED_FREE_DATASETS: List[Dict[str, Any]] = [
    {
        "id": "vaishnaviurnankar/indian-sign-language-dataset",
        "title": "Indian Sign Language Dataset (A-Z & Digits)",
        "language": "Indian Sign Language (ISL)",
        "license": "CC0: Public Domain",
        "estimated_size_mb": 42.0,
        "estimated_size_bytes": int(42.0 * 1024 * 1024),
        "estimated_images": 1200,
        "labels": ["A-Z", "0-9"],
        "is_free": True,
        "url": "https://www.kaggle.com/datasets/vaishnaviurnankar/indian-sign-language-dataset",
    },
    {
        "id": "prathumar/indian-sign-language-dataset",
        "title": "Indian Sign Language Alphabet & Word Signs",
        "language": "Indian Sign Language (ISL)",
        "license": "Open Data Commons (ODC)",
        "estimated_size_mb": 85.0,
        "estimated_size_bytes": int(85.0 * 1024 * 1024),
        "estimated_images": 2600,
        "labels": ["A-Z", "Gestures"],
        "is_free": True,
        "url": "https://www.kaggle.com/datasets/prathumar/indian-sign-language-dataset",
    },
    {
        "id": "ash257/indian-sign-language-dataset",
        "title": "ISL Hand Gestures for Single-Hand Fingerspelling",
        "language": "Indian Sign Language (ISL)",
        "license": "CC BY-SA 4.0",
        "estimated_size_mb": 115.0,
        "estimated_size_bytes": int(115.0 * 1024 * 1024),
        "estimated_images": 3500,
        "labels": ["A-Z"],
        "is_free": True,
        "url": "https://www.kaggle.com/datasets/ash257/indian-sign-language-dataset",
    },
    {
        "id": "grassknoted/asl-alphabet",
        "title": "ASL Alphabet Clean Static Landmarks Reference",
        "language": "American Sign Language (ASL Reference)",
        "license": "CC0: Public Domain",
        "estimated_size_mb": 1024.0,
        "estimated_size_bytes": int(1024.0 * 1024 * 1024),
        "estimated_images": 87000,
        "labels": ["A-Z", "del", "nothing", "space"],
        "is_free": True,
        "url": "https://www.kaggle.com/datasets/grassknoted/asl-alphabet",
    },
]


def load_manifest() -> Dict[str, Any]:
    """Loads persistent manifest of all downloaded and evaluated datasets."""
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": "1.0",
        "free_policy": "Strictly 100% Free — Zero Paid Services",
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "datasets": {},
    }


def save_manifest(manifest: Dict[str, Any]) -> None:
    """Saves updated manifest to disk."""
    manifest["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def has_kaggle_credentials() -> bool:
    """Checks whether Kaggle credentials exist on the host system without triggering sys.exit."""
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        return True
    if os.environ.get("KAGGLE_API_TOKEN"):
        return True
    home = os.path.expanduser("~")
    kaggle_dir = os.path.join(home, ".kaggle")
    if os.path.exists(os.path.join(kaggle_dir, "kaggle.json")) or os.path.exists(os.path.join(kaggle_dir, "access_token")):
        return True
    return False


def get_kaggle_api(tracker: ResourceBudgetTracker) -> Optional[Any]:
    """
    Attempts to initialize official Kaggle API safely without exiting process.
    Returns None if credentials are not configured or budget limit reached.
    """
    can_api, msg = tracker.check_can_api_request()
    if not can_api:
        print(f"[BUDGET LIMIT] {msg}")
        return None

    if not has_kaggle_credentials():
        return None

    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        tracker.record_api_request()
        return api
    except (SystemExit, Exception):
        # Credentials invalid or network failure
        return None


def search_kaggle_datasets(
    query: str,
    tracker: ResourceBudgetTracker,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """
    Searches Kaggle for public datasets matching the query within free limits.
    Falls back to curated free open-access datasets if Kaggle credentials are not provided.
    """
    results: List[Dict[str, Any]] = []
    api = get_kaggle_api(tracker)

    if api is not None:
        can_api, msg = tracker.check_can_api_request()
        if not can_api:
            print(f"[LIMIT REACHED] {msg}")
            return results

        try:
            print(f"[*] Querying official Kaggle API for '{query}' (Max {max_results} results)...")
            api_results = api.dataset_list(search=query, sort_by="relevance", page=1)
            tracker.record_api_request()

            for item in api_results[:max_results]:
                # Total size in bytes
                size_bytes = getattr(item, "totalBytes", None) or getattr(item, "size", 0)
                if isinstance(size_bytes, str):
                    try:
                        size_bytes = int(size_bytes)
                    except ValueError:
                        size_bytes = 0

                ref = getattr(item, "ref", str(item))
                title = getattr(item, "title", ref)
                license_name = getattr(item, "licenseName", "Public Free / Unknown")

                results.append({
                    "id": ref,
                    "title": title,
                    "language": "Sign Language",
                    "license": license_name,
                    "estimated_size_bytes": size_bytes,
                    "estimated_size_mb": round(size_bytes / (1024 * 1024), 2) if size_bytes else 0.0,
                    "is_free": True,
                    "source": "Kaggle API Search",
                    "url": f"https://www.kaggle.com/datasets/{ref}",
                })
        except Exception as ex:
            print(f"[WARNING] Kaggle API search encountered an error: {ex}")

    # If Kaggle API is unconfigured or returned 0 results, provide curated free datasets
    if not results:
        print("[*] Using verified free-access Indian Sign Language catalog...")
        for ds in CURATED_FREE_DATASETS[:max_results]:
            results.append({**ds, "source": "Curated Free Public Catalog"})

    return results


def download_dataset(
    dataset_info: Dict[str, Any],
    tracker: ResourceBudgetTracker,
    manifest: Dict[str, Any],
    dry_run: bool = False,
) -> bool:
    """
    Safely downloads a dataset archive verifying hard limits before downloading.
    """
    dataset_id = dataset_info["id"]
    size_bytes = dataset_info.get("estimated_size_bytes", 0)

    # 1. Check if already downloaded
    if dataset_id in manifest.get("datasets", {}) and manifest["datasets"][dataset_id].get("downloaded"):
        print(f"[SKIP] Dataset '{dataset_id}' already downloaded and tracked in manifest.")
        return True

    # 2. Check hard resource limits
    can_dl, reason = tracker.check_can_download(size_bytes)
    if not can_dl:
        print(f"[SKIPPED BY HARD LIMIT] '{dataset_id}': {reason}")
        # Record skipped reason in manifest
        manifest.setdefault("datasets", {})[dataset_id] = {
            "status": "SKIPPED",
            "reason": reason,
            "license": dataset_info.get("license", "Unknown"),
            "url": dataset_info.get("url", ""),
            "attempted_size_mb": dataset_info.get("estimated_size_mb", 0.0),
        }
        save_manifest(manifest)
        return False

    if dry_run:
        print(f"[DRY-RUN APPROVED] Dataset '{dataset_id}' ({dataset_info.get('estimated_size_mb', 0)} MB) is within remaining budget.")
        return True

    # 3. Perform download via Kaggle API with retries limit (Max 2)
    os.makedirs(RAW_DATASETS_DIR, exist_ok=True)
    api = get_kaggle_api(tracker)

    if api is None:
        print(f"[AUTH REQUIRED] Kaggle API credentials not found.")
        print(f"  To download '{dataset_id}', place your free 'kaggle.json' in '~/.kaggle/kaggle.json'")
        print(f"  (100% Free: Kaggle.com -> Account Settings -> Create New API Token).")
        manifest.setdefault("datasets", {})[dataset_id] = {
            "status": "AWAITING_CREDENTIALS",
            "reason": "Kaggle credentials not provided; download skipped without charges.",
            "url": dataset_info.get("url", ""),
            "license": dataset_info.get("license", "Unknown"),
        }
        save_manifest(manifest)
        return False

    success = False
    for attempt in range(1, MAX_DOWNLOAD_RETRIES + 1):
        try:
            print(f"[*] Downloading '{dataset_id}' (Attempt {attempt}/{MAX_DOWNLOAD_RETRIES})...")
            api.dataset_download_files(dataset_id, path=RAW_DATASETS_DIR, unzip=False, quiet=False)
            success = True
            break
        except Exception as e:
            print(f"[ERROR] Attempt {attempt} failed for '{dataset_id}': {e}")
            time.sleep(2)

    if success:
        # Verify downloaded file size
        actual_size = size_bytes
        zip_candidate = os.path.join(RAW_DATASETS_DIR, f"{dataset_id.split('/')[-1]}.zip")
        if os.path.exists(zip_candidate):
            actual_size = os.path.getsize(zip_candidate)

        tracker.record_download(dataset_id, actual_size, metadata=dataset_info)
        manifest.setdefault("datasets", {})[dataset_id] = {
            "status": "DOWNLOADED",
            "downloaded": True,
            "download_size_bytes": actual_size,
            "download_size_mb": round(actual_size / (1024 * 1024), 2),
            "archive_path": zip_candidate,
            "license": dataset_info.get("license", "Unknown"),
            "language": dataset_info.get("language", "Unknown"),
            "url": dataset_info.get("url", ""),
            "download_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        save_manifest(manifest)
        print(f"[SUCCESS] Downloaded '{dataset_id}' ({round(actual_size / (1024 * 1024), 2)} MB).")
        return True
    else:
        manifest.setdefault("datasets", {})[dataset_id] = {
            "status": "FAILED",
            "reason": f"Download failed after {MAX_DOWNLOAD_RETRIES} retries.",
            "url": dataset_info.get("url", ""),
        }
        save_manifest(manifest)
        return False


def main():
    parser = argparse.ArgumentParser(description="SignBridge Safe Free Dataset Collector")
    parser.add_argument("--query", type=str, default="indian sign language alphabet", help="Search query")
    parser.add_argument("--dry-run", action="store_true", help="Estimate storage and budget without downloading")
    parser.add_argument("--download", action="store_true", help="Download approved datasets")
    parser.add_argument("--status", action="store_true", help="Display current resource budget summary")
    args = parser.parse_args()

    tracker = ResourceBudgetTracker()
    manifest = load_manifest()
    summary = tracker.get_summary()

    print("=" * 70)
    print("SignBridge — Strictly Free Dataset Management & Budget Enforcer")
    print("=" * 70)
    print(f"• Download Budget Used:      {summary['downloaded_mb']} MB / {summary['max_download_mb']} MB ({summary['remaining_download_mb']} MB remaining)")
    print(f"• Extracted Storage Used:   {summary['extracted_mb']} MB / {summary['max_extracted_mb']} MB")
    print(f"• Datasets Downloaded:      {summary['datasets_downloaded']} / {summary['max_datasets']}")
    print(f"• Kaggle API Requests Used: {summary['api_requests']} / {summary['max_api_requests']}")
    print(f"• System Free Disk:         {summary['available_disk_gb']} GB")
    print("=" * 70)

    if args.status:
        return

    print(f"\n[1] Searching for datasets matching query: '{args.query}'...")
    candidates = search_kaggle_datasets(args.query, tracker, max_results=MAX_DATASETS)

    print(f"\nFound {len(candidates)} candidate datasets:")
    for idx, c in enumerate(candidates, 1):
        print(f"  {idx}. [{c['license']}] {c['id']} — ~{c.get('estimated_size_mb', 0)} MB")
        print(f"     URL: {c.get('url', '')}")

    print("\n[2] Evaluating against Hard Limits & Policies:")
    for c in candidates:
        if args.download or args.dry_run:
            download_dataset(c, tracker, manifest, dry_run=args.dry_run or (not args.download))

    final_summary = tracker.get_summary()
    print("\n" + "=" * 70)
    print("Execution Finished — Budget State:")
    print(f"• Downloaded: {final_summary['downloaded_mb']} MB ({final_summary['remaining_download_mb']} MB budget remaining)")
    print(f"• Manifest saved at: {MANIFEST_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()
