"""
Compatibility shim for backend.translator.
Directs imports to backend package.
"""

from backend.translator import *
from backend.translator import (
    EnglishToHindiTranslator,
    DEFAULT_MODEL_DIR,
)

__all__ = [
    "EnglishToHindiTranslator",
    "DEFAULT_MODEL_DIR",
]
