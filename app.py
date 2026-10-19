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

# On Windows 11, pre-importing torch before OpenCV/MediaPipe/scikit-learn
# ensures PyTorch's c10.dll and OpenMP runtimes initialize cleanly without WinError 1114.
try:
    import torch  # noqa: F401
except Exception:
    pass

import streamlit as st
from frontend.app import main

if __name__ == "__main__" or True:
    main()
