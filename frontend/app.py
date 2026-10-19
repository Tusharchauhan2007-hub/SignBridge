"""
SignBridge — Communication without barriers.
Main presentation layer entry point built with Streamlit.
Coordinates UI pages, navigation, styling, and connects to the backend processing pipeline.
"""

import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
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

from backend.data_collection import DatasetManager
from backend.hand_tracking import HandTracker
from backend.predictor import SignPredictor
from backend.preprocessing import LandmarkPreprocessor
from backend.text_to_speech import SentenceBuilder
from backend.translator import EnglishToHindiTranslator

from frontend.styles.theme import get_theme_css
from frontend.components.navbar import render_navbar
from frontend.components.footer import render_footer
from frontend.pages.home import render_home_page
from frontend.pages.how_it_works import render_how_it_works_page
from frontend.pages.features import render_features_page
from frontend.pages.live_app import render_live_app_page
from frontend.pages.studio import render_studio_page
from frontend.pages.about import render_about_page


# -----------------------------------------------------------------------------
# Streamlit Application Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SignBridge — Communication without barriers",
    page_icon="✋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Theme State Initialization (Support URL query params & session state persistence)
# -----------------------------------------------------------------------------
if "theme" not in st.session_state:
    try:
        q_theme = st.query_params.get("theme", None)
        st.session_state.theme = q_theme if q_theme in ("light", "dark") else "light"
    except Exception:
        st.session_state.theme = "light"

# Inject dynamic CSS design system
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "sentence_builder" not in st.session_state:
    st.session_state.sentence_builder = SentenceBuilder(cooldown_seconds=1.2)

if "tts_trigger_html" not in st.session_state:
    st.session_state.tts_trigger_html = ""

if "manual_text_input" not in st.session_state:
    st.session_state.manual_text_input = ""

if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

if "target_letter" not in st.session_state:
    st.session_state.target_letter = "A"

if "target_category" not in st.session_state:
    st.session_state.target_category = "Alphabet Letters (A–Z)"

if "last_recognized_sign" not in st.session_state:
    st.session_state.last_recognized_sign = None

if "translated_hindi_text" not in st.session_state:
    st.session_state.translated_hindi_text = ""

if "live_webcam_cap" not in st.session_state:
    st.session_state.live_webcam_cap = None

if "show_onboarding" not in st.session_state:
    st.session_state.show_onboarding = True

if "recognition_history" not in st.session_state:
    st.session_state.recognition_history = []

if "practice_target" not in st.session_state:
    st.session_state.practice_target = "A"

if "practice_matches" not in st.session_state:
    st.session_state.practice_matches = 0

if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False

if "text_font_size" not in st.session_state:
    st.session_state.text_font_size = "Large"

if "camera_source_idx" not in st.session_state:
    st.session_state.camera_source_idx = 0

if "demo_mode_active" not in st.session_state:
    st.session_state.demo_mode_active = False

if "last_added_sign_flash" not in st.session_state:
    st.session_state.last_added_sign_flash = ""

if "live_mode_view" not in st.session_state:
    st.session_state.live_mode_view = "Live Recognition"


# -----------------------------------------------------------------------------
# Cached Backend Resources
# -----------------------------------------------------------------------------
@st.cache_resource
def get_hand_tracker() -> HandTracker:
    """Cached HandTracker instance across reruns."""
    return HandTracker(max_num_hands=1)


@st.cache_resource
def get_preprocessor() -> LandmarkPreprocessor:
    """Cached LandmarkPreprocessor instance across reruns."""
    return LandmarkPreprocessor()


@st.cache_resource
def get_predictor() -> SignPredictor:
    """Cached SignPredictor instance with model file auto-discovery."""
    return SignPredictor()


@st.cache_resource
def get_dataset_manager() -> DatasetManager:
    """Cached DatasetManager managing data storage."""
    return DatasetManager()


@st.cache_resource
def get_translator() -> EnglishToHindiTranslator:
    """Cached offline EnglishToHindiTranslator."""
    return EnglishToHindiTranslator()


def main() -> None:
    """Main presentation router executing active page."""
    dataset_mgr = get_dataset_manager()
    predictor = get_predictor()

    # Global Navigation Bar & Theme Toggle
    render_navbar()

    # Active Page Routing
    current_page = st.session_state.get("active_page", "Home")

    if current_page == "Home":
        render_home_page(dataset_mgr, predictor)
    elif current_page == "How It Works":
        render_how_it_works_page()
    elif current_page == "Features":
        render_features_page()
    elif current_page == "Live App":
        sb: SentenceBuilder = st.session_state.sentence_builder
        preprocessor = get_preprocessor()
        tracker = get_hand_tracker()
        translator = get_translator()
        render_live_app_page(sb, preprocessor, tracker, predictor, translator)
    elif current_page == "Studio":
        preprocessor = get_preprocessor()
        tracker = get_hand_tracker()
        render_studio_page(dataset_mgr, preprocessor, tracker, predictor)
    elif current_page == "About":
        render_about_page()

    # Global Startup-Grade Footer
    render_footer()


if __name__ == "__main__":
    main()


