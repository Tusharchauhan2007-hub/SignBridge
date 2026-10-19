"""
Compatibility shim for backend.text_to_speech.
Directs imports to backend package.
"""

from backend.text_to_speech import *
from backend.text_to_speech import (
    SentenceBuilder,
    generate_web_speech_html,
    speak_pyttsx3,
)

__all__ = [
    "SentenceBuilder",
    "generate_web_speech_html",
    "speak_pyttsx3",
]
