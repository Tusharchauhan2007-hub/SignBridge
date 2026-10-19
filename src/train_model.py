"""
Compatibility shim for backend.train_model.
Directs imports to backend package.
"""

from backend.train_model import *
from backend.train_model import (
    ModelTrainer,
    DEFAULT_MODEL_DIR,
    DEFAULT_MODEL_FILE,
)

__all__ = [
    "ModelTrainer",
    "DEFAULT_MODEL_DIR",
    "DEFAULT_MODEL_FILE",
]
