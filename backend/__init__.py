"""
SignBridge Backend Package.
Provides core machine learning, computer vision, data collection, and translation services:
- Hand landmark tracking via MediaPipe Tasks HandLandmarker
- Coordinate preprocessing & 63-feature invariant normalization
- Multiclass Random Forest sign classification & prediction smoothing
- Dataset management & validation
- Debounced sentence construction & speech synthesis
- Offline local English-to-Hindi neural translation via MarianMT
"""

from backend.preprocessing import (
    LandmarkPreprocessor,
    TOTAL_FEATURES,
    NUM_LANDMARKS,
    NUM_COORDINATES,
    get_feature_names,
)
from backend.hand_tracking import (
    HandTracker,
    Landmark,
    HandLandmarks,
    HandDetectionResult,
    HAND_CONNECTIONS,
    DEFAULT_MODEL_DIR as DEFAULT_HAND_TRACKER_MODEL_DIR,
    DEFAULT_MODEL_PATH as DEFAULT_HAND_TRACKER_MODEL_PATH,
)
from backend.predictor import (
    SignPredictor,
    PredictionResult,
    DEFAULT_MODEL_DIR as DEFAULT_CLASSIFIER_MODEL_DIR,
    DEFAULT_MODEL_FILE as DEFAULT_CLASSIFIER_MODEL_FILE,
)
from backend.data_collection import (
    DatasetManager,
    CORE_ISL_GESTURES,
    ISL_ALPHABET_LETTERS,
    ALL_TARGET_CLASSES,
    ISL_ALPHABET_GUIDE,
    METADATA_COLUMNS,
    get_dataset_columns,
)
from backend.text_to_speech import (
    SentenceBuilder,
    generate_web_speech_html,
    speak_pyttsx3,
)
from backend.train_model import (
    ModelTrainer,
)
from backend.translator import (
    EnglishToHindiTranslator,
    DEFAULT_MODEL_DIR as DEFAULT_TRANSLATION_MODEL_DIR,
)

__all__ = [
    "LandmarkPreprocessor",
    "TOTAL_FEATURES",
    "NUM_LANDMARKS",
    "NUM_COORDINATES",
    "get_feature_names",
    "HandTracker",
    "Landmark",
    "HandLandmarks",
    "HandDetectionResult",
    "HAND_CONNECTIONS",
    "DEFAULT_HAND_TRACKER_MODEL_DIR",
    "DEFAULT_HAND_TRACKER_MODEL_PATH",
    "SignPredictor",
    "PredictionResult",
    "DEFAULT_CLASSIFIER_MODEL_DIR",
    "DEFAULT_CLASSIFIER_MODEL_FILE",
    "DatasetManager",
    "CORE_ISL_GESTURES",
    "ISL_ALPHABET_LETTERS",
    "ALL_TARGET_CLASSES",
    "ISL_ALPHABET_GUIDE",
    "METADATA_COLUMNS",
    "get_dataset_columns",
    "SentenceBuilder",
    "generate_web_speech_html",
    "speak_pyttsx3",
    "ModelTrainer",
    "EnglishToHindiTranslator",
    "DEFAULT_TRANSLATION_MODEL_DIR",
]

