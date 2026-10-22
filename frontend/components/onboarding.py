"""
Onboarding guide component for SignBridge.
Provides interactive step-by-step instructions for first-time signers.
Dark-tech card layout with monospace indicators.
"""

import streamlit as st


def render_onboarding_guide() -> None:
    """Renders the 3-step dismissible interactive onboarding card."""
    if st.session_state.get("show_onboarding", True):
        st.markdown(
            """
            <div class="sb-onboarding-card">
                <div class="sb-onboarding-header">
                    <div style="font-weight:600; font-size:0.95rem; color:var(--sb-text-main); display:flex; align-items:center; gap:0.5rem;">
                        <span class="sb-status-dot sb-dot-active"></span>
                        <span>QUICKSTART GUIDE // SIGNBRIDGE LIVE WORKSPACE</span>
                    </div>
                    <span style="font-family:'JetBrains Mono', monospace; font-size:0.72rem; color:var(--sb-text-muted);">[DISMISSIBLE GUIDE]</span>
                </div>
                <div class="sb-onboarding-grid">
                    <div class="sb-onboarding-step">
                        <div class="sb-onboarding-step-num">// STEP 01</div>
                        <div class="sb-onboarding-step-title">Position Hand in Optical View</div>
                        <div class="sb-onboarding-step-desc">Center hand 1.5–3 ft from your webcam. Good frontal lighting ensures sub-millimeter joint tracking.</div>
                    </div>
                    <div class="sb-onboarding-step">
                        <div class="sb-onboarding-step-num">// STEP 02</div>
                        <div class="sb-onboarding-step-title">Form Postures or Fingerspell</div>
                        <div class="sb-onboarding-step-desc">Hold steady for ~1 second. The 7-frame rolling buffer confirms gestures and appends letters into words.</div>
                    </div>
                    <div class="sb-onboarding-step">
                        <div class="sb-onboarding-step-num">// STEP 03</div>
                        <div class="sb-onboarding-step-title">Compose, Translate & Vocalize</div>
                        <div class="sb-onboarding-step-desc">Edit sentences with Space/Delete. Click <strong>Speak Sentence</strong> for dual TTS or <strong>Translate to Hindi</strong> for local MarianMT.</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
