"""
Offline English-to-Hindi Translation Engine for SignBridge.
Uses a local MarianMT neural translation model (Helsinki-NLP/opus-mt-en-hi) without cloud APIs.
"""
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

DEFAULT_MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "opus_mt_en_hi"


class EnglishToHindiTranslator:
    """
    Offline English-to-Hindi neural machine translator.
    Loads and runs entirely on local CPU via HuggingFace Transformers and PyTorch.
    Zero network calls are made during inference.
    """

    def __init__(self, model_dir: Optional[Path] = None):
        self.model_dir = Path(model_dir) if model_dir else DEFAULT_MODEL_DIR
        self._tokenizer = None
        self._model = None
        self._is_loaded = False
        self._load_error = None

    @property
    def is_available(self) -> bool:
        """Check if local model directory and required weight files exist."""
        if not self.model_dir.exists() or not self.model_dir.is_dir():
            return False
        required_files = ["config.json", "source.spm", "target.spm"]
        weights_exist = (self.model_dir / "model.safetensors").exists() or (self.model_dir / "pytorch_model.bin").exists()
        return weights_exist and all((self.model_dir / f).exists() for f in required_files)

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def load(self) -> Tuple[bool, Optional[str]]:
        """
        Load tokenizer and model weights from local disk.
        Returns (success: bool, error_message: Optional[str]).
        """
        if self._is_loaded:
            return True, None

        if not self.is_available:
            err = (
                f"Translation model files not found at '{self.model_dir}'. "
                "Please run `python download_translation_model.py` to set up offline translation."
            )
            self._load_error = err
            return False, err

        try:
            from transformers import MarianMTModel, MarianTokenizer

            self._tokenizer = MarianTokenizer.from_pretrained(
                str(self.model_dir),
                local_files_only=True,
            )
            self._model = MarianMTModel.from_pretrained(
                str(self.model_dir),
                local_files_only=True,
            )
            self._model.eval()
            self._is_loaded = True
            self._load_error = None
            return True, None
        except Exception as ex:
            err = f"Failed to load translation model: {ex}"
            logger.error(err, exc_info=True)
            self._load_error = err
            self._is_loaded = False
            return False, err

    def translate(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Translate an English string to Hindi (Devanagari).
        Returns (translated_text: Optional[str], error_message: Optional[str]).
        """
        if not text or not text.strip():
            return "", None

        clean_text = text.strip()

        if not self._is_loaded:
            success, err = self.load()
            if not success:
                return None, err

        try:
            import torch

            with torch.no_grad():
                inputs = self._tokenizer([clean_text], return_tensors="pt", padding=True, truncation=True)
                outputs = self._model.generate(
                    **inputs,
                    max_length=128,
                    num_beams=4,
                    early_stopping=True,
                )
                decoded = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
                return decoded.strip(), None
        except Exception as ex:
            err = f"Translation error: {ex}"
            logger.error(err, exc_info=True)
            return None, err
