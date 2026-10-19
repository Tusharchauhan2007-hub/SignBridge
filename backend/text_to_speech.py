"""
Text-to-Speech and Sentence Building module for SignBridge.
Provides sentence assembly with cooldown debouncing, token editing,
and dual TTS support: Python pyttsx3 backend thread and HTML5 Web Speech API for browsers.
"""

import html
import threading
import time
from typing import List, Optional

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False


class SentenceBuilder:
    """
    Sentence builder that manages tokens, spaces, cooldown debouncing, and text editing.
    """

    def __init__(self, cooldown_seconds: float = 1.2):
        self.tokens: List[str] = []
        self.cooldown_seconds = cooldown_seconds
        self.last_added_token: Optional[str] = None
        self.last_gesture_token: Optional[str] = None
        self.last_added_time: float = 0.0
        self.suppressed_after_clear: Optional[str] = None

    def can_append(self, token: str) -> bool:
        """Check if a token can be appended without immediate duplication or spamming."""
        if not token or not token.strip():
            return False
        clean = token.strip().upper()
        now = time.time()

        # If a sign was actively held when Clear was pressed, suppress re-adding that same sign
        if self.suppressed_after_clear is not None:
            if clean == self.suppressed_after_clear:
                return False
            # Gesture has changed to a different sign, release clear suppression
            self.suppressed_after_clear = None

        # Cooldown check: if same token as last gesture or last added token, require cooldown
        check_token = self.last_gesture_token if self.last_gesture_token is not None else self.last_added_token
        if check_token and clean == check_token and (now - self.last_added_time) < self.cooldown_seconds:
            return False

        return True

    def append_token(self, token: str, force: bool = False) -> bool:
        """Append token if debounced cooldown condition is met (or if force=True)."""
        if not token or not token.strip():
            return False
        clean = token.strip().upper()
        if not force and not self.can_append(clean):
            return False
        self.tokens.append(clean)
        self.last_added_token = clean
        self.last_gesture_token = clean
        self.last_added_time = time.time()
        self.suppressed_after_clear = None
        return True

    def append_space(self) -> None:
        """Add an explicit space token."""
        self.tokens.append(" ")
        self.last_added_token = " "
        self.last_added_time = time.time()
        self.suppressed_after_clear = None

    def backspace(self, current_sign: Optional[str] = None) -> None:
        """
        Remove exactly the last character from the composed text.
        If the text is empty, do nothing without raising an exception.
        Suppresses the currently held sign so auto-add doesn't immediately re-add it.
        """
        if not self.tokens:
            return

        last = self.tokens[-1]
        if last == " ":
            self.tokens.pop()
        elif len(last) > 1:
            # Word token: remove the last character
            trimmed = last[:-1]
            if trimmed.endswith("_"):
                trimmed = trimmed[:-1]
            if trimmed:
                self.tokens[-1] = trimmed
            else:
                self.tokens.pop()
        else:
            # Single character token
            self.tokens.pop()

        self.last_added_token = self.tokens[-1] if self.tokens else None
        non_spaces = [t for t in self.tokens if t != " "]
        self.last_gesture_token = non_spaces[-1] if non_spaces else None
        self.last_added_time = time.time()

        # Suppress re-adding the currently visible sign until hand is lowered or changed
        token_to_suppress = current_sign or self.last_gesture_token or self.last_added_token
        if token_to_suppress and token_to_suppress != " ":
            self.suppressed_after_clear = token_to_suppress.strip().upper()

    def clear(self, current_sign: Optional[str] = None) -> None:
        """
        Clear all tokens.
        Suppresses immediate re-addition of the currently visible sign until
        hand is lowered or sign changes.
        """
        self.tokens.clear()
        token_to_suppress = current_sign or self.last_gesture_token or self.last_added_token
        if token_to_suppress and token_to_suppress != " ":
            self.suppressed_after_clear = token_to_suppress.strip().upper()
        else:
            self.suppressed_after_clear = None
        self.last_added_token = None
        self.last_added_time = 0.0

    def notify_no_hand(self) -> None:
        """Notify sentence builder that no hand is detected in current frame."""
        self.suppressed_after_clear = None
        self.last_gesture_token = None

    def get_text(self) -> str:
        """
        Construct full readable sentence from tokens.
        - Single letters (A-Z) concatenate directly into words (e.g. ['C', 'A', 'T'] -> 'CAT').
        - Multi-letter words (e.g. 'HELLO', 'YES') are automatically separated by spaces.
        - Underscores in word signs (e.g. 'THANK_YOU') are converted to spaces ('THANK YOU').
        - Explicit space tokens ' ' create word boundaries and preserve trailing spaces.
        """
        if not self.tokens:
            return ""

        output = ""
        prev_is_single_letter = False

        for t in self.tokens:
            if t == " ":
                output += " "
                prev_is_single_letter = False
                continue

            cleaned_token = t.replace("_", " ").strip()
            if not cleaned_token:
                continue

            is_single_letter = len(cleaned_token) == 1 and cleaned_token.isalpha()

            if not output:
                output += cleaned_token
            elif output.endswith(" "):
                output += cleaned_token
            elif prev_is_single_letter and is_single_letter:
                # Consecutive single letters form a word directly (e.g. 'C' + 'A' + 'T' -> 'CAT')
                output += cleaned_token
            else:
                # Separate word gestures or words by space
                output += " " + cleaned_token

            prev_is_single_letter = is_single_letter

        return output




def speak_pyttsx3(text: str) -> None:
    """Speak text using pyttsx3 in an isolated thread to prevent blocking the UI loop."""
    if not HAS_PYTTSX3 or not text.strip():
        return

    def _worker():
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[SignBridge] TTS error: {e}")

    threading.Thread(target=_worker, daemon=True).start()


def generate_web_speech_html(text: str, trigger_id: str = "") -> str:
    """
    Generate an HTML5 Web Speech API script that plays audio natively in the user's browser.
    This works reliably across all client devices without server-side soundcard limitations.
    """
    safe_text = html.escape(text.replace('"', '\\"').replace("\n", " "))
    return f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var utterance = new SpeechSynthesisUtterance("{safe_text}");
                utterance.rate = 0.95;
                utterance.pitch = 1.0;
                utterance.lang = 'en-US';
                window.speechSynthesis.speak(utterance);
            }}
        }})();
    </script>
    """

