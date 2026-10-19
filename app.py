"""
SignBridge — Communication without barriers.
Root application launcher forwarding to the modular frontend and backend packages.
"""

import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Prioritize project virtual environment site-packages if running outside venv
VENV_SITE_PACKAGES = PROJECT_ROOT / ".venv" / "Lib" / "site-packages"
if VENV_SITE_PACKAGES.exists() and str(VENV_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(VENV_SITE_PACKAGES))

# Add .venv MediaPipe C bindings DLL path to Windows DLL search directory
VENV_MEDIAPIPE_C = VENV_SITE_PACKAGES / "mediapipe" / "tasks" / "c"
if VENV_MEDIAPIPE_C.exists() and hasattr(os, "add_dll_directory"):
    try:
        os.add_dll_directory(str(VENV_MEDIAPIPE_C))
    except Exception:
        pass

# On Windows 11, pre-importing torch before OpenCV/MediaPipe/scikit-learn
# ensures PyTorch's c10.dll and OpenMP runtimes initialize cleanly without WinError 1114.
try:
    import torch  # noqa: F401
except Exception:
    pass

import streamlit as st
from frontend.app import main

if __name__ == "__main__":
    main()

