"""
Features page for SignBridge.
Details core accessibility tech capabilities and features.
"""

import streamlit as st


def render_features_page() -> None:
    """Renders the Features overview page."""
    st.markdown(
        """
        <div class="sb-section-tag">Product Capabilities</div>
        <h1 class="sb-section-heading">Designed for Everyday Accessibility</h1>
        <p class="sb-section-desc">
            Thoughtfully built to empower individuals who use sign language with immediate, natural communication tools.
        </p>
        """,
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns(3, gap="medium")
    with f1:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">VISION</div>
                <div class="sb-step-title">Real-Time Hand Tracking</div>
                <div class="sb-step-text">
                    Continuous 30 FPS skeleton tracking with visual feedback, wrist references, and finger-joint indicators.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">ALPHABET</div>
                <div class="sb-step-title">A–Z Fingerspelling</div>
                <div class="sb-step-text">
                    Support for individual letters allowing signers to spell out names, locations, and specific words naturally.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">SYNTAX</div>
                <div class="sb-step-title">Sentence Assembly</div>
                <div class="sb-step-text">
                    Letters automatically merge into complete words, while spaces and word signs maintain clean punctuation.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    f4, f5, f6 = st.columns(3, gap="medium")
    with f4:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">SPEECH</div>
                <div class="sb-step-title">Dual Speech Synthesis</div>
                <div class="sb-step-text">
                    Universal voice output using both native backend audio (pyttsx3) and browser-native HTML5 Web Speech.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f5:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">STUDIO</div>
                <div class="sb-step-title">In-App Dataset Collector</div>
                <div class="sb-step-text">
                    Capture authentic training samples with session metadata, participant IDs, and class balance tracking.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f6:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">SAFETY</div>
                <div class="sb-step-title">Confidence Gating</div>
                <div class="sb-step-text">
                    Refuses to invent false predictions when lighting is poor or hand posture confidence is below threshold.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

