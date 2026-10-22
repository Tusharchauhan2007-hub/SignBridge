"""
Offline Hindi Translation Component for SignBridge.
Integrates local MarianMT neural translation model with instant copy & dismiss controls.
Dark-tech card layout with monospace telemetry, language flow, and Devanagari display.
"""

import html
import json
import streamlit as st
from backend.text_to_speech import SentenceBuilder
from backend.translator import EnglishToHindiTranslator


def _copy_to_clipboard(text: str) -> None:
    """Injects client-side clipboard writer supporting modern navigator.clipboard and fallback."""
    escaped = json.dumps(text)
    js = f"""
    <script>
    (function() {{
        var text = {escaped};
        function fallback() {{
            var ta = document.createElement("textarea");
            ta.value = text;
            ta.style.position = "fixed";
            ta.style.left = "-9999px";
            ta.style.top = "-9999px";
            document.body.appendChild(ta);
            ta.focus();
            ta.select();
            try {{ document.execCommand("copy"); }} catch (e) {{}}
            document.body.removeChild(ta);
        }}
        if (navigator.clipboard && window.isSecureContext) {{
            navigator.clipboard.writeText(text).catch(fallback);
        }} else {{
            fallback();
        }}
    }})();
    </script>
    """
    st.components.v1.html(js, height=0)


def render_translation_display() -> None:
    """Renders the translated Hindi output card beneath the composed sentence."""
    if st.session_state.get("translated_hindi_text"):
        hi_text = st.session_state.translated_hindi_text
        st.markdown(
            f"""
            <div class="sb-translation-container">
                <div class="sb-translation-header">
                    <div style="display:flex; align-items:center; gap:0.5rem;">
                        <span class="sb-status-dot sb-dot-ready"></span>
                        <span class="sb-translation-badge">LOCAL SEQ2SEQ // HINDI (हिंदी)</span>
                    </div>
                    <span style="font-family:'JetBrains Mono', monospace; font-size:0.72rem; color:#999999;">
                        EN ──► HI • 100% OFFLINE MARIANMT
                    </span>
                </div>
                <div class="sb-translation-output">{html.escape(hi_text)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c_hi_copy, c_hi_clear = st.columns([1.6, 1])
        with c_hi_copy:
            if st.button("Copy Hindi Translation", key="copy_hindi_btn", use_container_width=True):
                _copy_to_clipboard(hi_text)
                st.toast(f"Copied Hindi to clipboard: '{hi_text}'")
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
