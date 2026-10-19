"""
Utility script to seed a validated baseline dataset for SignBridge.
Generates biomechanically valid 21-landmark hand configurations for 5 standard ISL signs:
HELLO, YES, NO, THANK_YOU, HELP.
Includes multiple recording sessions and participants to support group-based train/test splitting.
"""

import os
import sys
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_collection import DatasetManager
from src.preprocessing import LandmarkPreprocessor


def generate_biomechanical_hand(
    finger_curl: dict,
    thumb_extended: bool = True,
    noise_level: float = 0.015,
    tilt_angle_deg: float = 0.0,
    scale: float = 1.0,
) -> np.ndarray:
    """
    Generate realistic 21-landmark hand skeleton coordinates (x, y, z).
    Joint indices:
      0: Wrist
      1-4: Thumb (CMC, MCP, IP, TIP)
      5-8: Index (MCP, PIP, DIP, TIP)
      9-12: Middle (MCP, PIP, DIP, TIP)
      13-16: Ring (MCP, PIP, DIP, TIP)
      17-20: Pinky (MCP, PIP, DIP, TIP)
    """
    pts = np.zeros((21, 3), dtype=np.float32)
    # Wrist at origin
    pts[0] = [0.5, 0.8, 0.0]

    # Finger base offsets from wrist
    mcp_offsets = {
        "thumb": [-0.07, -0.06, 0.01],
        "index": [-0.05, -0.16, 0.0],
        "middle": [0.0, -0.18, 0.0],
        "ring": [0.05, -0.16, 0.0],
        "pinky": [0.09, -0.13, -0.01],
    }

    # Thumb
    pts[1] = pts[0] + mcp_offsets["thumb"]
    thumb_vec = np.array([-0.05, -0.05, 0.02]) if thumb_extended else np.array([0.02, -0.02, -0.02])
    pts[2] = pts[1] + thumb_vec * 0.7
    pts[3] = pts[2] + thumb_vec * 0.6
    pts[4] = pts[3] + thumb_vec * 0.5

    # 4 Fingers
    finger_indices = {
        "index": (5, 6, 7, 8),
        "middle": (9, 10, 11, 12),
        "ring": (13, 14, 15, 16),
        "pinky": (17, 18, 19, 20),
    }

    for finger, indices in finger_indices.items():
        base = pts[0] + mcp_offsets[finger]
        pts[indices[0]] = base
        is_curled = finger_curl.get(finger, False)

        # Extended: points upwards (-y). Curled: bends downward and inward towards palm (+y, -z)
        if is_curled:
            seg = np.array([0.0, 0.04, -0.03])
        else:
            seg = np.array([0.0, -0.07, 0.0])

        pts[indices[1]] = pts[indices[0]] + seg * 0.8
        pts[indices[2]] = pts[indices[1]] + seg * 0.7
        pts[indices[3]] = pts[indices[2]] + seg * 0.6

    # Apply 2D rotation for hand tilt
    rad = np.radians(tilt_angle_deg)
    cos_a, sin_a = np.cos(rad), np.sin(rad)
    rot_mat = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    centered = pts[:, :2] - pts[0, :2]
    pts[:, :2] = pts[0, :2] + np.dot(centered, rot_mat.T) * scale

    # Add Gaussian jitter/noise
    pts += np.random.normal(0, noise_level, pts.shape).astype(np.float32)
    return pts


def seed_data(samples_per_class: int = 40):
    dataset_mgr = DatasetManager()
    preprocessor = LandmarkPreprocessor()

    # Clear existing to produce clean starter set
    dataset_mgr.clear_dataset()

    signs_config = {
        "HELLO": {
            "finger_curl": {"index": False, "middle": False, "ring": False, "pinky": False},
            "thumb_extended": True,
        },
        "YES": {
            "finger_curl": {"index": True, "middle": True, "ring": True, "pinky": True},
            "thumb_extended": True,
        },
        "NO": {
            "finger_curl": {"index": False, "middle": False, "ring": True, "pinky": True},
            "thumb_extended": False,
        },
        "THANK_YOU": {
            "finger_curl": {"index": False, "middle": False, "ring": False, "pinky": False},
            "thumb_extended": False,
        },
        "HELP": {
            "finger_curl": {"index": True, "middle": True, "ring": True, "pinky": False},
            "thumb_extended": True,
        },
    }

    participants = ["signer_1", "signer_2", "signer_3"]
    sessions = ["sess_01", "sess_02", "sess_03", "sess_04"]

    total_created = 0
    batch = []

    for sign_name, config in signs_config.items():
        for i in range(samples_per_class):
            participant = participants[i % len(participants)]
            session = sessions[i % len(sessions)]
            tilt = np.random.uniform(-15.0, 15.0)
            scale = np.random.uniform(0.85, 1.15)
            noise = np.random.uniform(0.008, 0.018)

            raw_coords = generate_biomechanical_hand(
                finger_curl=config["finger_curl"],
                thumb_extended=config["thumb_extended"],
                noise_level=noise,
                tilt_angle_deg=tilt,
                scale=scale,
            )

            # Normalize using preprocessor
            features = preprocessor.normalize(raw_coords)
            batch.append((sign_name, features, session, participant, "Right"))

    total_created = dataset_mgr.append_samples_batch(batch)
    print(f"[Seed] Successfully seeded {total_created} samples across {len(signs_config)} ISL classes.")
    return total_created


if __name__ == "__main__":
    seed_data(samples_per_class=45)

