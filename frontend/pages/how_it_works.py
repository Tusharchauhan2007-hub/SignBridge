"""
How It Works page for SignBridge.
Explains the 3-step edge computer vision and ML pipeline.
"""

import streamlit as st


def render_how_it_works_page() -> None:
    """Renders the How It Works educational page."""
    st.markdown(
        """
        <div class="sb-section-tag">System Architecture</div>
        <h1 class="sb-section-heading">How SignBridge Works</h1>
        <p class="sb-section-desc">
            A comprehensive, privacy-first computer vision and machine learning pipeline
            tailored for assistive communication.
        </p>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">01 / CAPTURE</div>
                <div class="sb-step-title">Hand Landmark Detection</div>
                <div class="sb-step-text">
                    Using Google MediaPipe Tasks API, the system detects 21 hand landmarks
                    per frame with sub-millimeter normalized precision (x, y, z coordinates).
                    Frames are mirrored for an intuitive signer experience.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">02 / NORMALIZE</div>
                <div class="sb-step-title">Geometric Invariance</div>
                <div class="sb-step-text">
                    Raw coordinates are transformed relative to the wrist (landmark 0) and scaled
                    by the distance to the middle finger joint. This makes recognition invariant
                    to camera distance, framing, or hand scale.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="sb-step-card">
                <div class="sb-step-num">03 / STABILIZE</div>
                <div class="sb-step-title">Window Debouncing & Speech</div>
                <div class="sb-step-text">
                    A rolling 7-frame majority voting buffer eliminates video flicker.
                    Recognized letters assemble into full words, while temporal debouncing
                    prevents identical characters from repeating unintentionally.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sb-callout" style="padding: 1.75rem;">
            <div class="sb-callout-title" style="font-size: 1.15rem; margin-bottom: 0.6rem;">
                Machine Learning Architecture
            </div>
            <div class="sb-callout-text" style="font-size: 0.92rem; line-height: 1.65;">
                SignBridge uses a Random Forest Classifier with balanced class weighting. Unlike black-box neural networks,
                geometric Random Forests evaluate joint angles directly, run at over 60 FPS on standard CPUs,
                and prevent data leakage using session-based cross-validation (<code>GroupShuffleSplit</code>).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

