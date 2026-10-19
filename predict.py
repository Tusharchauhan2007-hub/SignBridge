"""
SignBridge — Standalone Prediction Utility.
Loads trained classifier artifact and predicts Indian Sign Language gestures and
alphabet letters from static images, CSV samples, or feature arrays.
"""

import argparse
import os
import sys
from typing import Optional

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import cv2
import numpy as np

from config import MODELS_DIR, PROCESSED_DATA_PATH
try:
    from backend.data_collection import DatasetManager
    from backend.hand_tracking import HandTracker
    from backend.predictor import SignPredictor
    from backend.preprocessing import LandmarkPreprocessor, get_feature_names
except ImportError:
    from src.data_collection import DatasetManager
    from src.hand_tracking import HandTracker
    from src.predictor import SignPredictor
    from src.preprocessing import LandmarkPreprocessor, get_feature_names


def predict_from_image(image_path: str, predictor: SignPredictor) -> None:
    """Detects hand landmarks in an image and runs prediction."""
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return

    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Failed to read image: {image_path}")
        return

    tracker = HandTracker(max_num_hands=1)
    preprocessor = LandmarkPreprocessor()

    print(f"[*] Analyzing image '{os.path.basename(image_path)}' ({img.shape[1]}x{img.shape[0]})...")
    detection = tracker.detect(img)

    if not detection.has_hand or not detection.hands:
        print("[RESULT] No hand detected in image.")
        return

    landmarks = detection.hands[0].landmarks
    features = preprocessor.extract_from_landmarks(landmarks)

    if features is None:
        print("[RESULT] Failed to extract geometric features.")
        return

    prediction = predictor.predict(features)
    print("\n" + "=" * 50)
    print("SignBridge Prediction Result:")
    print("=" * 50)
    print(f"• Predicted Sign:   {prediction.label}")
    print(f"• Confidence Score: {prediction.confidence * 100:.1f}%")
    print(f"• Classification:   {'Valid High Confidence' if prediction.is_valid else 'Low Confidence (Below Gating Threshold)'}")
    print(f"• Handedness:       {detection.hands[0].handedness or 'Right'}")

    if prediction.probabilities:
        print("\nTop 5 Class Probabilities:")
        sorted_probs = sorted(prediction.probabilities.items(), key=lambda x: x[1], reverse=True)[:5]
        for cls, prob in sorted_probs:
            bar = "█" * int(prob * 20)
            print(f"  • {cls:<10} {prob * 100:5.1f}% {bar}")
    print("=" * 50)


def predict_from_csv_sample(sample_idx: int, predictor: SignPredictor) -> None:
    """Loads a specific row from isl_dataset.csv and evaluates prediction."""
    dataset_mgr = DatasetManager(PROCESSED_DATA_PATH)
    df = dataset_mgr.load_dataset()

    if df.empty:
        print("[ERROR] Dataset is empty.")
        return

    if sample_idx < 0 or sample_idx >= len(df):
        print(f"[ERROR] Sample index {sample_idx} out of range (0 to {len(df) - 1}).")
        return

    row = df.iloc[sample_idx]
    actual_label = row["label"]
    feature_cols = get_feature_names()
    features = row[feature_cols].to_numpy(dtype=np.float32)

    prediction = predictor.predict(features)

    print("\n" + "=" * 50)
    print(f"CSV Sample Evaluation (Index {sample_idx}):")
    print("=" * 50)
    print(f"• Actual Ground Truth: {actual_label}")
    print(f"• Model Prediction:    {prediction.label}")
    print(f"• Confidence:          {prediction.confidence * 100:.1f}%")
    print(f"• Match:               {'CORRECT (MATCH)' if actual_label == prediction.label else 'MISMATCH'}")
    print("=" * 50)


def display_model_status(predictor: SignPredictor) -> None:
    """Displays information on the loaded model and recognized classes."""
    print("=" * 70)
    print("SignBridge Model Status")
    print("=" * 70)
    if not predictor.is_loaded:
        print("[STATUS] No classifier model currently loaded.")
        print(f"Run 'python train_model.py' to train a model.")
    else:
        print(f"• Model File:            {predictor.model_path}")
        print(f"• Total Classes ({len(predictor.classes)}):    {', '.join(predictor.classes)}")
        print(f"• Confidence Threshold: {predictor.confidence_threshold * 100:.0f}%")
        print(f"• Temporal Smoothing:   7-frame majority voting buffer active")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="SignBridge Standalone Predictor")
    parser.add_argument("--image", type=str, help="Path to static hand image for prediction")
    parser.add_argument("--sample", type=int, help="Index of row from isl_dataset.csv to test")
    parser.add_argument("--threshold", type=float, default=0.60, help="Confidence threshold (0.0 to 1.0)")
    parser.add_argument("--status", action="store_true", help="Display model status and active classes")
    args = parser.parse_args()

    predictor = SignPredictor(confidence_threshold=args.threshold)

    if args.status or (not args.image and args.sample is None):
        display_model_status(predictor)
        if not args.image and args.sample is None:
            return

    if args.image:
        predict_from_image(args.image, predictor)
    elif args.sample is not None:
        predict_from_csv_sample(args.sample, predictor)


if __name__ == "__main__":
    main()

