"""
Offline Hindi Translation Component for SignBridge.
Integrates local MarianMT neural translation model with instant copy & dismiss controls.
"""

import html
import streamlit as st
from backend.text_to_speech import SentenceBuilder
from backend.translator import EnglishToHindiTranslator


def render_translation_display() -> None:
    """Renders the translated Hindi output card beneath the composed sentence."""
    if st.session_state.get("translated_hindi_text"):
        hi_text = st.session_state.translated_hindi_text
        st.markdown(
            f"""
            <div class="sb-translation-container">
                <div class="sb-translation-header">
                    <span class="sb-translation-badge">HINDI (हिंदी अनुवाद)</span>
                    <span style="font-size:0.74rem; color:var(--sb-text-subtle);">100% Offline • MarianMT</span>
                </div>
                <div class="sb-translation-output">{html.escape(hi_text)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c_hi_copy, c_hi_clear = st.columns([1.6, 1])
        with c_hi_copy:
            if st.button("Copy Hindi Translation", key="copy_hindi_btn", use_container_width=True):
                st.toast(f"Copied Hindi: '{hi_text}'")
        with c_hi_clear:
            if st.button("Dismiss Translation", key="dismiss_hindi_btn", use_container_width=True):
                st.session_state.translated_hindi_text = ""
                st.rerun()


def handle_translation_trigger(sb: SentenceBuilder, translator: EnglishToHindiTranslator) -> None:
    """Processes translation request on the currently composed sentence."""
    curr_to_trans = sb.get_text()
    if not curr_to_trans or not curr_to_trans.strip():
        st.warning("Cannot translate an empty sentence. Sign or spell some words first.")
    else:
        if not translator.is_available:
            st.error("Offline translation model files not found at `models/opus_mt_en_hi`.")
            st.info(
                "Please run this command in PowerShell to set up the offline translation model:\n\n"
                "```powershell\n"
                "python download_translation_model.py\n"
                "```"
            )
        else:
            with st.spinner("Translating to Hindi (offline)..."):
                hi_res, err = translator.translate(curr_to_trans)
                if err:
                    st.error(f"Translation failed: {err}")
                else:
                    st.session_state.translated_hindi_text = hi_res
                    st.rerun()

