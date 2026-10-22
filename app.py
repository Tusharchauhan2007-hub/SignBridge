"""
SignBridge — Communication without barriers.
Root application launcher forwarding to the modular frontend and backend packages.
Guarantees session state, theme initialization, and dynamic styling injection on every rerun.
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

try:
    st.set_page_config(
        page_title="SignBridge — AI Sign Recognition & Translation",
        page_icon="✋",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
except Exception:
    pass

from frontend.app import main as frontend_main, init_app_session_state
from frontend.styles.theme import get_theme_css

# Ensure theme state initialization exists for root app
if "theme" not in st.session_state:
    try:
        q_theme = st.query_params.get("theme", None)
        st.session_state.theme = q_theme if q_theme in ("light", "dark") else "dark"
    except Exception:
        st.session_state.theme = "dark"

try:
    if st.query_params.get("theme") != st.session_state.theme:
        st.query_params["theme"] = st.session_state.theme
except Exception:
    pass


def main() -> None:
    """Main application runner."""
    init_app_session_state()
    frontend_main()


if __name__ == "__main__":
    main()
