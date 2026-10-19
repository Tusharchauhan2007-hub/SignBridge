"""
About page for SignBridge.
Details product philosophy, technology stack, and creator credits.
"""

import streamlit as st


def render_about_page() -> None:
    """Renders the About & Ethics page with creator credits."""
    st.markdown(
        """
        <div class="sb-section-tag">Organization & Ethics</div>
        <h1 class="sb-section-heading">About SignBridge</h1>
        <p class="sb-section-desc">
            Bridging communication gaps through transparent, human-centered assistive technology.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        ### Our Product Philosophy
        SignBridge was designed on the principle that assistive communication technology should be:
        1. **Locally Executed & Private**: Video frames remain on the client device and are never transmitted to external cloud servers.
        2. **Transparent About Limitations**: Sign languages are rich, complex natural languages containing grammar, facial expressions, and dynamic motion. SignBridge translates defined static hand postures and fingerspelling without pretending to replace certified human interpreters.
        3. **Linguistically Grounded**: We respect the linguistic distinction between Indian Sign Language (ISL) and American Sign Language (ASL).
        
        ---
        
        ### Project Authorship
        **SignBridge** is an assistive AI accessibility initiative created and developed by:
        - **Tushar Chauhan**
        - **Ujjwal Dhiman**

        Made by Tushar Chauhan and Ujjwal Dhiman.
        *A project by Tushar Chauhan and Ujjwal Dhiman, engineered for real-time edge sign recognition.*

        ---
        
        ### Technology Stack
        - **Computer Vision**: OpenCV + Google MediaPipe Tasks HandLandmarker (`hand_landmarker.task`).
        - **Feature Engineering**: 63 wrist-relative translation-invariant and scale-invariant 3D features.
        - **Machine Learning**: Balanced Random Forest with session-based `GroupShuffleSplit`.
        - **Speech Synthesis**: Offline SAPI/pyttsx3 engine paired with HTML5 Web Speech API.
        - **Offline Neural Translation**: Helsinki-NLP MarianMT English-to-Hindi seq2seq transformer running on local CPU.
        """
    )

