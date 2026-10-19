"""
Sentence composition controls and editing toolbar for SignBridge.
Manages token manipulation, space insertion, backspacing, and vocalization.
"""

from datetime import datetime
import html
import streamlit as st
from backend.text_to_speech import SentenceBuilder, generate_web_speech_html, speak_pyttsx3
from backend.translator import EnglishToHindiTranslator
from frontend.components.translation_card import handle_translation_trigger


def _cb_add_sign():
    curr = st.session_state.get("last_recognized_sign")
    if curr:
        st.session_state.sentence_builder.append_token(curr, force=True)
        st.session_state.last_added_sign_flash = curr
        st.session_state.recognition_history.insert(0, {
            "sign": curr,
            "time": datetime.now().strftime("%H:%M:%S"),
            "confidence": 1.0,
            "source": "Manual Add",
        })
        st.session_state.recognition_history = st.session_state.recognition_history[:30]


def _cb_space():
    st.session_state.sentence_builder.append_space()
    st.session_state.last_added_sign_flash = "Space"


def _cb_delete():
    curr = st.session_state.get("last_recognized_sign")
    st.session_state.sentence_builder.backspace(current_sign=curr)
    st.session_state.last_added_sign_flash = "Delete"
    if not st.session_state.sentence_builder.get_text():
        st.session_state.translated_hindi_text = ""


def _cb_clear():
    curr = st.session_state.get("last_recognized_sign")
    st.session_state.sentence_builder.clear(current_sign=curr)
    st.session_state.last_recognized_sign = None
    st.session_state.translated_hindi_text = ""
    st.session_state.confirm_clear = False
    st.session_state.last_added_sign_flash = ""


def _cb_request_clear():
    if st.session_state.sentence_builder.get_text():
        st.session_state.confirm_clear = True
    else:
        _cb_clear()


def render_sentence_controls(sb: SentenceBuilder, translator: EnglishToHindiTranslator) -> None:
    """Renders the complete communication output console and action toolbars."""
    # Action callbacks for instant, atomic updates without breaking camera loops
    st.markdown(
        """
        <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle); margin-top:0.6rem; margin-bottom:0.4rem;">
            Sentence Editing
        </div>
        """,
        unsafe_allow_html=True,
    )
    a_add, a_spc, a_del, a_clr = st.columns([1.2, 1, 1, 1])
    with a_add:
        curr_last = st.session_state.get("last_recognized_sign")
        add_label = f"Add '{curr_last}'" if curr_last else "Add Sign"
        st.button(
            add_label,
            use_container_width=True,
            key="live_add_btn",
            disabled=not bool(curr_last),
            on_click=_cb_add_sign,
        )
    with a_spc:
        st.button(
            "Space",
            use_container_width=True,
            key="live_space",
            on_click=_cb_space,
        )
    with a_del:
        st.button(
            "Delete",
            use_container_width=True,
            key="live_del",
            on_click=_cb_delete,
        )
    with a_clr:
        st.button(
            "Clear",
            use_container_width=True,
            key="live_clear",
            on_click=_cb_request_clear,
        )

    # Confirmation required before clearing non-empty messages
    if st.session_state.get("confirm_clear", False):
        st.markdown(
            """
            <div style="background:var(--sb-warning-bg); border:1px solid var(--sb-warning-border); border-radius:6px; padding:0.65rem 0.85rem; margin-top:0.5rem; margin-bottom:0.5rem;">
                <span style="font-size:0.82rem; font-weight:600; color:var(--sb-text-main);">Clear entire composed message?</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        cc_col1, cc_col2 = st.columns(2)
        with cc_col1:
            st.button("Yes, Clear Message", type="primary", use_container_width=True, key="confirm_clear_yes_btn", on_click=_cb_clear)
        with cc_col2:
            if st.button("Cancel", use_container_width=True, key="confirm_clear_cancel_btn"):
                st.session_state.confirm_clear = False
                st.rerun()

    # Secondary toolbar: Copy, Speech Vocalization & Offline Hindi Translation
    st.markdown(
        """
        <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle); margin-top:0.9rem; margin-bottom:0.4rem;">
            Actions & Speech
        </div>
        """,
        unsafe_allow_html=True,
    )
    c_copy, c_speak, c_trans = st.columns([1, 1.4, 1.6])
    with c_copy:
        if st.button("Copy Text", use_container_width=True, key="live_copy"):
            txt = sb.get_text()
            if txt:
                st.toast(f"Copied: '{txt}'")
            else:
                st.toast("Sentence is empty.")
    with c_speak:
        if st.button("Speak Sentence", type="primary", use_container_width=True, key="live_speak"):
            curr_to_speak = sb.get_text()
            if curr_to_speak:
                speak_pyttsx3(curr_to_speak)
                st.session_state.tts_trigger_html = generate_web_speech_html(curr_to_speak)
                st.success(f"Speaking: '{curr_to_speak}'")
            else:
                st.warning("Cannot speak an empty sentence.")
    with c_trans:
        if st.button("Translate to Hindi", use_container_width=True, key="live_translate_btn"):
            handle_translation_trigger(sb, translator)

    if st.session_state.tts_trigger_html:
        st.components.v1.html(st.session_state.tts_trigger_html, height=0)
        st.session_state.tts_trigger_html = ""

