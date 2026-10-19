"""
Onboarding guide component for SignBridge.
Provides interactive step-by-step instructions for first-time signers.
"""

import streamlit as st


def render_onboarding_guide() -> None:
    """Renders the 3-step dismissible interactive onboarding card."""
    if st.session_state.get("show_onboarding", True):
        st.markdown(
            """
            <div class="sb-onboarding-card">
                <div class="sb-onboarding-header">
                    <div style="font-weight:700; font-size:0.98rem; color:var(--sb-text-main);">
                        Getting Started with SignBridge Live
                    </div>
                    <span style="font-size:0.75rem; color:var(--sb-text-subtle);">First-Time User Guide</span>
                </div>
                <div class="sb-onboarding-grid">
                    <div class="sb-onboarding-step">
                        <div class="sb-onboarding-step-num">STEP 01</div>
                        <div class="sb-onboarding-step-title">Position Hand</div>
                        <div class="sb-onboarding-step-desc">Center your hand 1.5–3 ft from your webcam. Good lighting and a plain background maximize tracking accuracy.</div>
                    </div>
                    <div class="sb-onboarding-step">
                        <div class="sb-onboarding-step-num">STEP 02</div>
                        <div class="sb-onboarding-step-title">Sign or Fingerspell</div>
                        <div class="sb-onboarding-step-desc">Hold your hand posture steady for ~1 second. Recognized letters concatenate automatically into words.</div>
                    </div>
                    <div class="sb-onboarding-step">
                        <div class="sb-onboarding-step-num">STEP 03</div>
                        <div class="sb-onboarding-step-title">Compose & Speak</div>
                        <div class="sb-onboarding-step-desc">Use Space/Delete to edit. Click <strong>Speak Sentence</strong> for audio vocalization, or <strong>Translate to Hindi</strong> for local translation.</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

