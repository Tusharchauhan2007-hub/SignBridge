"""
Live Recognition Workspace and Interactive Practice Mode for SignBridge.
Coordinates real-time webcam inference, hand landmark overlay, sentence building,
offline Hindi translation, speech synthesis, and guided ISL posture training.
"""

from datetime import datetime
import html
import time
import cv2
import streamlit as st

from backend.data_collection import ISL_ALPHABET_LETTERS, ISL_ALPHABET_GUIDE
from backend.hand_tracking import HandTracker
from backend.predictor import SignPredictor
from backend.preprocessing import LandmarkPreprocessor
from backend.text_to_speech import SentenceBuilder, generate_web_speech_html, speak_pyttsx3
from backend.translator import EnglishToHindiTranslator
from frontend.components.onboarding import render_onboarding_guide
from frontend.components.telemetry import render_positioning_tips
from frontend.components.translation_card import render_translation_display, handle_translation_trigger
from frontend.components.sentence_controls import (
    render_sentence_controls,
    _cb_add_sign,
    _cb_space,
    _cb_delete,
    _cb_clear,
)


def render_live_app_page(
    sb: SentenceBuilder,
    preprocessor: LandmarkPreprocessor,
    tracker: HandTracker,
    predictor: SignPredictor,
    translator: EnglishToHindiTranslator,
) -> None:
    """Renders the complete SignBridge Live assistive workspace."""
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:1.25rem;">
            <div>
                <div class="sb-section-tag">Assistive Workspace</div>
                <h2 style="font-size:1.85rem; font-weight:800; letter-spacing:-0.03em; margin:0; color:var(--sb-text-main);">SignBridge Live</h2>
            </div>
            <div style="display:flex; align-items:center; gap:0.75rem;">
                <span style="font-size:0.82rem; color:var(--sb-text-subtle);">
                    Client-Side Inference • Offline Capable
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Workspace Navigation / Mode Selection Toolbar
    m_col1, m_col2, m_col3 = st.columns([2.2, 1.2, 1.2])
    with m_col1:
        current_mode = st.session_state.get("live_mode_view", "Live Recognition")
        if st.session_state.get("live_mode_selector") != current_mode:
            st.session_state.live_mode_selector = current_mode

        mode_choice = st.radio(
            "Workspace Mode",
            options=["Live Recognition", "Interactive Practice Mode"],
            index=0 if current_mode == "Live Recognition" else 1,
            horizontal=True,
            key="live_mode_selector",
            label_visibility="collapsed",
        )
        if mode_choice != st.session_state.get("live_mode_view"):
            st.session_state.live_mode_view = mode_choice
            st.rerun()

    with m_col2:
        demo_btn_label = "Exit Demo Mode" if st.session_state.get("demo_mode_active", False) else "Try Demo Mode"
        if st.button(demo_btn_label, use_container_width=True, key="demo_mode_toggle_btn"):
            st.session_state.demo_mode_active = not st.session_state.get("demo_mode_active", False)
            st.rerun()

    with m_col3:
        if st.session_state.get("show_onboarding", True):
            if st.button("Hide Guide", use_container_width=True, key="toggle_onboarding_hide_btn"):
                st.session_state.show_onboarding = False
                st.rerun()
        else:
            if st.button("Show Guide", use_container_width=True, key="toggle_onboarding_show_btn"):
                st.session_state.show_onboarding = True
                st.rerun()

    # 1. Dismissible Interactive Onboarding Guide
    render_onboarding_guide()

    # 2. Interactive Demo Mode Banner (Simulated Input without Camera)
    if st.session_state.get("demo_mode_active", False):
        st.markdown(
            """
            <div class="sb-demo-banner">
                <div>
                    <span class="sb-demo-badge">DEMO MODE ACTIVE</span>
                    <strong style="margin-left:0.5rem; color:var(--sb-text-main); font-size:0.88rem;">Hardware Camera Bypassed</strong>
                    <div style="font-size:0.8rem; color:var(--sb-text-muted); margin-top:0.2rem;">
                        Click any simulated sign token below to test sentence composition, speech vocalization, and offline Hindi translation immediately.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle); margin-bottom:0.4rem;">
                Simulated Gesture Controls (Click to emit token)
            </div>
            """,
            unsafe_allow_html=True,
        )
        demo_letters = ["H", "E", "L", "O", "W", "R", "D"]
        demo_words = ["HELLO", "YES", "NO", "THANK_YOU", "HELP"]
        d_cols = st.columns(len(demo_letters) + len(demo_words))
        for idx, letter in enumerate(demo_letters):
            with d_cols[idx]:
                if st.button(letter, key=f"demo_sign_{letter}", use_container_width=True):
                    sb.append_token(letter, force=True)
                    st.session_state.last_recognized_sign = letter
                    st.session_state.last_added_sign_flash = letter
                    st.session_state.recognition_history.insert(0, {
                        "sign": letter,
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "confidence": 0.98,
                        "source": "Demo Simulation",
                    })
                    st.session_state.recognition_history = st.session_state.recognition_history[:30]
                    st.rerun()

        for idx, word in enumerate(demo_words):
            with d_cols[len(demo_letters) + idx]:
                display_label = word.replace("_", " ")
                if st.button(display_label, key=f"demo_sign_{word}", use_container_width=True):
                    sb.append_token(word, force=True)
                    st.session_state.last_recognized_sign = word
                    st.session_state.last_added_sign_flash = word
                    st.session_state.recognition_history.insert(0, {
                        "sign": word,
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "confidence": 0.99,
                        "source": "Demo Simulation",
                    })
                    st.session_state.recognition_history = st.session_state.recognition_history[:30]
                    st.rerun()
        st.markdown("<hr style='margin:1rem 0; border:none; border-top:1px dashed var(--sb-border);'>", unsafe_allow_html=True)

    # 3. Interactive Practice Mode vs Standard Live Recognition Workspace
    if st.session_state.get("live_mode_view") == "Interactive Practice Mode":
        st.markdown(
            """
            <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle); margin-bottom:0.5rem;">
                Guided Posture Trainer (ISL Alphabet)
            </div>
            """,
            unsafe_allow_html=True,
        )

        p_col_left, p_col_right = st.columns([1.25, 1], gap="large")

        with p_col_left:
            p_cam_col1, p_cam_col2 = st.columns([1.2, 1.8])
            with p_cam_col1:
                run_practice_cam = st.toggle("Activate Practice Camera", value=False, key="run_practice_cam_toggle")
            with p_cam_col2:
                p_thresh = st.slider("Match Confidence", 0.40, 0.95, 0.60, 0.05, key="practice_conf_slider")
                predictor.confidence_threshold = p_thresh

            p_cam_placeholder = st.empty()
            p_error_placeholder = st.empty()
            p_match_badge_placeholder = st.empty()

        with p_col_right:
            curr_target = st.session_state.get("practice_target", "A")
            target_desc = ISL_ALPHABET_GUIDE.get(curr_target, "Form the target hand shape clearly towards the camera.")

            st.markdown(
                f"""
                <div class="sb-practice-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
                        <div>
                            <span style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle);">Current Target</span>
                            <div class="sb-practice-target">{curr_target}</div>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle);">Matches Today</span>
                            <div style="font-size:1.5rem; font-weight:800; color:var(--sb-success);">{st.session_state.get("practice_matches", 0)}</div>
                        </div>
                    </div>
                    <div style="font-weight:600; font-size:0.9rem; color:var(--sb-text-main); margin-bottom:0.35rem;">Posture Instruction:</div>
                    <div style="font-size:0.85rem; color:var(--sb-text-muted); line-height:1.5; margin-bottom:1rem;">{target_desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            p_nav_col1, p_nav_col2 = st.columns([1.5, 1])
            with p_nav_col1:
                sel_target = st.selectbox(
                    "Switch Target Letter",
                    options=ISL_ALPHABET_LETTERS,
                    index=ISL_ALPHABET_LETTERS.index(curr_target) if curr_target in ISL_ALPHABET_LETTERS else 0,
                    key="practice_letter_select",
                )
                if sel_target != curr_target:
                    st.session_state.practice_target = sel_target
                    st.rerun()
            with p_nav_col2:
                if st.button("Next Letter →", use_container_width=True, key="next_target_letter_btn"):
                    curr_idx = ISL_ALPHABET_LETTERS.index(curr_target) if curr_target in ISL_ALPHABET_LETTERS else -1
                    next_idx = (curr_idx + 1) % len(ISL_ALPHABET_LETTERS)
                    st.session_state.practice_target = ISL_ALPHABET_LETTERS[next_idx]
                    st.rerun()

            p_feedback_placeholder = st.empty()
            p_feedback_placeholder.info(f"Form letter **{curr_target}** in front of your camera. When recognized, your score increases!")

        # Practice Camera Loop
        if run_practice_cam:
            cap = st.session_state.get("live_webcam_cap")
            if cap is None or not cap.isOpened():
                try:
                    cam_idx = st.session_state.get("camera_source_idx", 0)
                    try:
                        cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
                    except Exception:
                        cap = None
                    if cap is None or not cap.isOpened():
                        cap = cv2.VideoCapture(cam_idx)
                    if not cap.isOpened():
                        cap = cv2.VideoCapture(0)
                    if cap.isOpened():
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        st.session_state.live_webcam_cap = cap
                except Exception:
                    cap = None

            if cap is None or not cap.isOpened():
                p_error_placeholder.error("Webcam connection failed. Please ensure camera permissions are granted.")
            else:
                try:
                    matched_this_session = False
                    while run_practice_cam:
                        ret, frame = cap.read()
                        if not ret:
                            time.sleep(0.04)
                            continue

                        frame = cv2.flip(frame, 1)
                        detection = tracker.detect(frame)
                        features = None
                        if detection.has_hand and detection.hands:
                            features = preprocessor.extract_from_landmarks(detection.hands[0].landmarks)

                        annotated = tracker.draw_landmarks(frame, detection)
                        pred = predictor.predict(features)

                        p_cam_placeholder.image(
                            cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
                            channels="RGB",
                            use_container_width=True,
                        )

                        target = st.session_state.get("practice_target", "A")
                        if pred.is_valid:
                            if pred.label == target:
                                p_match_badge_placeholder.markdown(
                                    f'<div class="sb-badge-detected sb-badge-success">✓ MATCH: {pred.label} ({int(pred.confidence * 100)}%)</div>',
                                    unsafe_allow_html=True,
                                )
                                p_feedback_placeholder.success(f"🎯 Perfect! Posture for letter **{target}** matched with {int(pred.confidence * 100)}% confidence.")
                                if not matched_this_session:
                                    st.session_state.practice_matches = st.session_state.get("practice_matches", 0) + 1
                                    matched_this_session = True
                            else:
                                p_match_badge_placeholder.markdown(
                                    f'<div class="sb-badge-detected sb-badge-warning">Detected: {pred.label} • Need: {target}</div>',
                                    unsafe_allow_html=True,
                                )
                                p_feedback_placeholder.warning(f"Detected **{pred.label}**. Adjust your fingers to match the posture instructions for **{target}**.")
                        elif pred.label == "No hand detected":
                            p_match_badge_placeholder.markdown(
                                '<div class="sb-badge-detected sb-badge-neutral">Position Hand in Frame</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            p_match_badge_placeholder.markdown(
                                f'<div class="sb-badge-detected sb-badge-neutral">Low Confidence ({int(pred.confidence * 100)}%)</div>',
                                unsafe_allow_html=True,
                            )

                        time.sleep(0.03)
                except Exception as e:
                    p_error_placeholder.error(f"Practice error: {e}")
                finally:
                    if not st.session_state.get("run_practice_cam_toggle", False) or st.session_state.get("live_mode_view") != "Interactive Practice Mode":
                        if st.session_state.get("live_webcam_cap") is not None:
                            try:
                                st.session_state.live_webcam_cap.release()
                            except Exception:
                                pass
                            st.session_state.live_webcam_cap = None
        else:
            if st.session_state.get("live_webcam_cap") is not None:
                try:
                    st.session_state.live_webcam_cap.release()
                except Exception:
                    pass
                st.session_state.live_webcam_cap = None
            p_cam_placeholder.markdown(
                """
                <div class="sb-cam-offline">
                    <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:12px;">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="m10 8 4 4-4 4"/>
                    </svg>
                    <div style="font-weight:600; color:#e2e8f0; font-size:1rem; margin-bottom:4px;">Practice Camera Idle</div>
                    <div style="color:#94a3b8; font-size:0.88rem;">Toggle <strong>Activate Practice Camera</strong> above to test your signs against the reference.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:
        # Standard Live Recognition Workspace
        col_cam, col_console = st.columns([1.25, 1], gap="large")

        with col_cam:
            st.markdown(
                """
                <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle); margin-bottom:0.5rem;">
                    Camera & Detection Settings
                </div>
                """,
                unsafe_allow_html=True,
            )
            c_tool1, c_tool2, c_tool3 = st.columns([1.2, 1.2, 1.6])
            with c_tool1:
                run_camera = st.toggle("Activate Camera", value=False, key="run_cam_toggle")
            with c_tool2:
                auto_add = st.checkbox("Auto-add to Sentence", value=True)
            with c_tool3:
                conf_threshold = st.slider("Confidence Gating", 0.40, 0.95, 0.60, 0.05)
                predictor.confidence_threshold = conf_threshold

            # Switch camera source control
            cam_src_col1, cam_src_col2 = st.columns([1.6, 1])
            with cam_src_col1:
                cam_choice = st.selectbox(
                    "Camera Device",
                    options=[0, 1],
                    format_func=lambda x: f"Camera {x} (Default / Integrated)" if x == 0 else f"Camera {x} (External / USB)",
                    index=st.session_state.get("camera_source_idx", 0),
                    key="camera_source_select",
                    help="Switch between default built-in camera and external USB webcam.",
                )
                if cam_choice != st.session_state.get("camera_source_idx", 0):
                    st.session_state.camera_source_idx = cam_choice
                    if st.session_state.get("live_webcam_cap") is not None:
                        try:
                            st.session_state.live_webcam_cap.release()
                        except Exception:
                            pass
                        st.session_state.live_webcam_cap = None
                    st.rerun()

            cam_feed_placeholder = st.empty()
            error_placeholder = st.empty()

            pred_badge_placeholder = st.empty()
            conf_bar_placeholder = st.empty()

            render_positioning_tips()

        with col_console:
            st.markdown(
                """
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
                    <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle);">
                        Communication Output
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            fs_col1, fs_col2 = st.columns([1.6, 1.4])
            with fs_col1:
                size_choice = st.radio(
                    "Display Size",
                    options=["Normal", "Large", "XL"],
                    index=["Normal", "Large", "XL"].index(st.session_state.get("text_font_size", "Large")),
                    horizontal=True,
                    key="font_size_selector",
                )
                st.session_state.text_font_size = size_choice
            with fs_col2:
                flash_sign = st.session_state.get("last_added_sign_flash", "")
                if flash_sign:
                    st.markdown(f'<div style="text-align:right; margin-top:0.5rem;"><span class="sb-added-pulse">✓ Added \'{html.escape(flash_sign)}\'</span></div>', unsafe_allow_html=True)

            sentence_box_placeholder = st.empty()
            token_stream_placeholder = st.empty()

            render_translation_display()

            # Check model status
            if predictor.is_loaded:
                active_alpha = [c for c in predictor.classes if c in ISL_ALPHABET_LETTERS]
                if not active_alpha:
                    st.info(
                        "Alphabet Data Needed: Active model recognizes "
                        f"**{len(predictor.classes)}** word signs ({', '.join(predictor.classes)}). "
                        "To recognize A–Z fingerspelling, record letters in **Studio** and retrain."
                    )
            else:
                st.warning("No trained classifier model loaded. Please visit **Studio** to train a model.")

            render_sentence_controls(sb, translator)

            # Session Recognition History Drawer
            rec_history = st.session_state.get("recognition_history", [])
            with st.expander(f"Session Recognition History ({len(rec_history)} events)", expanded=False):
                if not rec_history:
                    st.markdown("<span style='font-size:0.82rem; color:var(--sb-text-subtle);'>No signs recorded in this session yet. Start signing or use Demo Mode.</span>", unsafe_allow_html=True)
                else:
                    hist_html = ['<div style="display:flex; flex-wrap:wrap; gap:4px; max-height:160px; overflow-y:auto; padding:4px 0;">']
                    for h_item in rec_history[:25]:
                        hist_html.append(
                            f'<div class="sb-history-chip">'
                            f'<span class="sb-history-sign">{html.escape(h_item.get("sign", ""))}</span>'
                            f'<span class="sb-history-meta">{h_item.get("time", "")} • {int(h_item.get("confidence", 1.0) * 100)}%</span>'
                            f'</div>'
                        )
                    hist_html.append('</div>')
                    st.markdown("".join(hist_html), unsafe_allow_html=True)
                    if st.button("Clear History", key="clear_rec_history_btn"):
                        st.session_state.recognition_history = []
                        st.rerun()

            with st.expander("Quick Gesture & Alphabet Guide"):
                st.markdown(
                    """
                    - **Fingerspelling (A–Z)**: Hold your hand steady; consecutive letters automatically spell out words.
                    - **Space**: Click `Space` or pause between words.
                    - **Delete**: Removes the last character one by one cleanly.
                    - **Core ISL Words**: `HELLO`, `YES`, `NO`, `THANK_YOU`, `HELP`.
                    - **Offline Hindi Translation**: Click `Translate to Hindi` to translate your composed sentence to Hindi using the local neural model.
                    """
                )

        font_style_map = {
            "Normal": "font-size:1.15rem; min-height:95px;",
            "Large": "font-size:1.45rem; min-height:115px;",
            "XL": "font-size:1.85rem; min-height:135px;",
        }
        current_font_style = font_style_map.get(st.session_state.get("text_font_size", "Large"), "font-size:1.45rem; min-height:115px;")

        curr_initial_text = sb.get_text()
        init_display = html.escape(curr_initial_text) if curr_initial_text else '<span style="color:var(--sb-text-muted);">Start signing or fingerspelling to construct your sentence...</span>'
        sentence_box_placeholder.markdown(f'<div class="sb-sentence-output" style="{current_font_style}">{init_display}</div>', unsafe_allow_html=True)
        pred_badge_placeholder.markdown('<div class="sb-badge-detected sb-badge-neutral">Ready • Awaiting Hand</div>', unsafe_allow_html=True)

        # Live Camera Processing Loop
        if run_camera:
            cap = st.session_state.get("live_webcam_cap")
            if cap is None or not cap.isOpened():
                try:
                    cam_idx = st.session_state.get("camera_source_idx", 0)
                    try:
                        cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
                    except Exception:
                        cap = None

                    if cap is None or not cap.isOpened():
                        cap = cv2.VideoCapture(cam_idx)
                    if not cap.isOpened():
                        cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        cap = cv2.VideoCapture(1)

                    if cap.isOpened():
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        st.session_state.live_webcam_cap = cap
                except Exception:
                    cap = None

            if cap is None or not cap.isOpened():
                error_placeholder.error("Webcam connection failed. Please ensure camera permissions are granted.")
            else:
                try:
                    while run_camera:
                        ret, frame = cap.read()
                        if not ret:
                            time.sleep(0.04)
                            continue

                        frame = cv2.flip(frame, 1)

                        detection = tracker.detect(frame)
                        features = None
                        if detection.has_hand and detection.hands:
                            features = preprocessor.extract_from_landmarks(detection.hands[0].landmarks)

                        annotated = tracker.draw_landmarks(frame, detection)
                        pred = predictor.predict(features)

                        cam_feed_placeholder.image(
                            cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
                            channels="RGB",
                            use_container_width=True,
                        )

                        if pred.is_valid:
                            st.session_state.last_recognized_sign = pred.label
                            badge_html = f'<div class="sb-badge-detected sb-badge-success">{pred.label} • {int(pred.confidence * 100)}%</div>'
                            pred_badge_placeholder.markdown(badge_html, unsafe_allow_html=True)
                            conf_bar_placeholder.progress(min(1.0, max(0.0, pred.confidence)), text=f"Confidence: {int(pred.confidence * 100)}%")
                            if auto_add:
                                before_txt = sb.get_text()
                                sb.append_token(pred.label)
                                after_txt = sb.get_text()
                                if after_txt != before_txt:
                                    st.session_state.last_added_sign_flash = pred.label
                                    st.session_state.recognition_history.insert(0, {
                                        "sign": pred.label,
                                        "time": datetime.now().strftime("%H:%M:%S"),
                                        "confidence": float(pred.confidence),
                                        "source": "Camera Live",
                                    })
                                    st.session_state.recognition_history = st.session_state.recognition_history[:30]
                        elif pred.label == "No hand detected":
                            st.session_state.last_recognized_sign = None
                            sb.notify_no_hand()
                            pred_badge_placeholder.markdown('<div class="sb-badge-detected sb-badge-neutral">No Hand Detected</div>', unsafe_allow_html=True)
                            conf_bar_placeholder.progress(0.0, text="Position hand within frame")
                        else:
                            st.session_state.last_recognized_sign = None
                            badge_html = f'<div class="sb-badge-detected sb-badge-warning">{pred.label} • {int(pred.confidence * 100)}%</div>'
                            pred_badge_placeholder.markdown(badge_html, unsafe_allow_html=True)
                            conf_bar_placeholder.progress(min(1.0, max(0.0, pred.confidence)), text="Below confidence threshold")

                        live_text = sb.get_text()
                        live_display = html.escape(live_text) if live_text else '<span style="color:var(--sb-text-muted);">Start signing or fingerspelling to construct your sentence...</span>'
                        sentence_box_placeholder.markdown(f'<div class="sb-sentence-output" style="{current_font_style}">{live_display}</div>', unsafe_allow_html=True)

                        time.sleep(0.03)

                except Exception as e:
                    error_placeholder.error(f"Live processing error: {e}")
                finally:
                    if not st.session_state.get("run_cam_toggle", False) or st.session_state.get("active_page") != "Live App":
                        if st.session_state.get("live_webcam_cap") is not None:
                            try:
                                st.session_state.live_webcam_cap.release()
                            except Exception:
                                pass
                            st.session_state.live_webcam_cap = None
        else:
            if st.session_state.get("live_webcam_cap") is not None:
                try:
                    st.session_state.live_webcam_cap.release()
                except Exception:
                    pass
                st.session_state.live_webcam_cap = None
            cam_feed_placeholder.markdown(
                """
                <div class="sb-cam-offline">
                    <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:12px;">
                        <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>
                        <circle cx="12" cy="13" r="3"/>
                    </svg>
                    <div style="font-weight:600; color:#e2e8f0; font-size:1rem; margin-bottom:4px;">Camera is Idle</div>
                    <div style="color:#94a3b8; font-size:0.88rem;">Toggle <strong>Activate Camera</strong> above to start recognition.</div>
                    <div style="font-size:0.78rem; color:#64748b; margin-top:8px;">All processing remains local. No video is recorded or streamed.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

