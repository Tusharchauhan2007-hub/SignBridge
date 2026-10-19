"""
Offline Translation Model Downloader for SignBridge.
Downloads Helsinki-NLP/opus-mt-en-hi and saves all model weights & tokenizer
files locally into models/opus_mt_en_hi for 100% offline translation.
"""
import sys
from pathlib import Path

MODEL_ID = "Helsinki-NLP/opus-mt-en-hi"
TARGET_DIR = Path(__file__).resolve().parent / "models" / "opus_mt_en_hi"


def download_model(force: bool = False):
    print("=" * 60)
    print("SignBridge — Offline English-to-Hindi Translation Model Setup")
    print("=" * 60)
    print(f"Target Directory: {TARGET_DIR}")
    print(f"Pretrained Model: {MODEL_ID}")
    print("License: CC-BY-4.0 (Open-source, free for research & production)")
    print("Storage requirement: ~304 MB")
    print("RAM requirement: ~450 MB (runs on standard CPU)")
    print("-" * 60)

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    weights_file = TARGET_DIR / "model.safetensors"
    config_file = TARGET_DIR / "config.json"
    spm_file = TARGET_DIR / "source.spm"

    if not force and weights_file.exists() and config_file.exists() and spm_file.exists():
        print(f"Model already downloaded at '{TARGET_DIR}'.")
        print("Verifying offline load...")
    else:
        try:
            from transformers import MarianMTModel, MarianTokenizer
        except ImportError:
            print("ERROR: 'transformers' or 'torch' is not installed.")
            print("Please run: pip install torch --index-url https://download.pytorch.org/whl/cpu")
            print("            pip install transformers sentencepiece sacremoses")
            sys.exit(1)

        print(f"Downloading '{MODEL_ID}' from HuggingFace...")
        tokenizer = MarianTokenizer.from_pretrained(MODEL_ID)
        model = MarianMTModel.from_pretrained(MODEL_ID)

        print(f"Saving weights and tokenizer to {TARGET_DIR}...")
        tokenizer.save_pretrained(str(TARGET_DIR))
        model.save_pretrained(str(TARGET_DIR))
        print("Download and local save complete.")

    # Verification test
    try:
        try:
            from backend.translator import EnglishToHindiTranslator
        except ImportError:
            from src.translator import EnglishToHindiTranslator

        print("Testing local offline translation...")
        translator = EnglishToHindiTranslator(model_dir=TARGET_DIR)
        success, err = translator.load()
        if not success:
            print(f"Verification failed: {err}")
            sys.exit(1)

        test_sentences = [
            "Hello, how are you?",
            "I need help",
            "Thank you",
        ]
        for s in test_sentences:
            hi, err = translator.translate(s)
            if err:
                print(f"Error on '{s}': {err}")
            else:
                # Encode safely for Windows console
                print(f"  [EN] {s} -> [HI] {hi}")

        print("-" * 60)
        print("Offline English-to-Hindi translator is READY and verified!")
        print("=" * 60)
    except Exception as ex:
        print(f"Verification error: {ex}")
        sys.exit(1)


if __name__ == "__main__":
    force_download = "--force" in sys.argv
    download_model(force=force_download)

