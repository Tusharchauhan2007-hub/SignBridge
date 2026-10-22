"""
About page for SignBridge.
Details product philosophy, technology stack, and creator credits.
Modern dark-tech card layout with monospace indicators, glassmorphic panels, and verified authorship.
"""

import streamlit as st


def render_about_page() -> None:
    """Renders the About & Ethics page with creator credits."""
    st.markdown(
        """
        <div class="sb-section-tag">// ETHICS & SYSTEM PROVENANCE</div>
        <h1 class="sb-section-heading">About SignBridge</h1>
        <p class="sb-section-desc">
            Bridging communication gaps through transparent, human-centered assistive technology and local edge intelligence.
        </p>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1.2, 1], gap="large")

    with c1:
        st.markdown(
            """
            ### Our Product Philosophy
            SignBridge was designed on the principle that assistive communication technology should be:
            1. **Locally Executed & Private**: Video frames remain on the client device and are never transmitted to external cloud servers.
            2. **Transparent About Limitations**: Sign languages are rich, complex natural languages containing grammar, facial expressions, and dynamic motion. SignBridge translates defined static hand postures and fingerspelling without pretending to replace certified human interpreters.
            3. **Linguistically Grounded**: We respect the linguistic distinction between Indian Sign Language (ISL) and American Sign Language (ASL).
            4. **User-Configurable & Accessible**: Empowers signers to define their own custom voice macros and emergency action shortcuts.
            """
        )

        st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)

        st.markdown(
            """
            ### Project Authorship
            **SignBridge** is an assistive AI accessibility initiative created and developed by:
            - **Tushar Chauhan**
            - **Ujjwal Dhiman**

            Made with care by Tushar Chauhan and Ujjwal Dhiman.
            *A project by Tushar Chauhan and Ujjwal Dhiman, engineered for real-time edge sign recognition.*
            """
        )

    with c2:
        st.markdown(
            """
            <div class="sb-callout" style="padding:1.5rem; margin-bottom:1rem;">
                <div class="sb-callout-title" style="font-size:1.1rem; color:#818cf8;">
                    <span class="sb-status-dot sb-dot-active"></span>
                    <span>Technology Stack</span>
                </div>
                <div style="font-size:0.86rem; color:var(--sb-text-muted); line-height:1.7; margin-top:0.75rem;">
                    • <strong>Computer Vision:</strong> OpenCV + Google MediaPipe Tasks HandLandmarker (<code>hand_landmarker.task</code>).<br>
                    • <strong>Feature Engineering:</strong> 63 wrist-relative translation-invariant and scale-invariant 3D features.<br>
                    • <strong>Machine Learning:</strong> Balanced Random Forest with session-based <code>GroupShuffleSplit</code>.<br>
                    • <strong>Speech Synthesis:</strong> Offline SAPI/pyttsx3 engine paired with HTML5 Web Speech API.<br>
                    • <strong>Offline Neural Translation:</strong> Helsinki-NLP MarianMT English-to-Hindi seq2seq transformer running on local CPU.<br>
                    • <strong>Macro Automation:</strong> Local JSON custom command engine for personalized assistance.
                </div>
            </div>
            <div class="sb-callout" style="padding:1.5rem;">
                <div class="sb-callout-title" style="font-size:1.1rem; color:#10b981;">
                    <span class="sb-status-dot sb-dot-ready"></span>
                    <span>Offline Guarantee</span>
                </div>
                <div style="font-size:0.86rem; color:var(--sb-text-muted); line-height:1.6; margin-top:0.75rem;">
                    SignBridge strictly enforces a hard resource ceiling and zero paid APIs policy. No credentials, tokens, or video frames leave your laptop.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
