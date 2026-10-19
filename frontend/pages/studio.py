"""
Studio page for SignBridge: Dataset Collection & Model Training.
Enables collecting labeled hand landmarks, viewing alphabet coverage,
and training local Random Forest models.
"""
from datetime import datetime
import time
import cv2
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from backend.data_collection import (
    DatasetManager,
    CORE_ISL_GESTURES,
    ISL_ALPHABET_LETTERS,
    ALL_TARGET_CLASSES,
    ISL_ALPHABET_GUIDE,
)
from backend.hand_tracking import HandTracker
from backend.predictor import SignPredictor
from backend.preprocessing import LandmarkPreprocessor
from backend.train_model import ModelTrainer


def render_studio_page(
    dataset_mgr: DatasetManager,
    preprocessor: LandmarkPreprocessor,
    tracker: HandTracker,
    predictor: SignPredictor,
) -> None:
    """Renders the dataset collection and model training studio interface."""
    st.markdown(
        """
        <div class="sb-section-tag">Machine Learning Operations</div>
        <h1 class="sb-section-heading">SignBridge Studio</h1>
        <p class="sb-section-desc">
            Collect verified hand landmark coordinates, evaluate dataset integrity, and train custom Random Forest models.
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    tab_data, tab_train = st.tabs(["1. Dataset Collection (Aâ€“Z & Gestures)", "2. Model Training & Evaluation"])
    
    # Sub-Tab 1: Dataset Collection
    with tab_data:
        col_d_left, col_d_right = st.columns([1.1, 1.4], gap="large")
    
        with col_d_left:
            st.markdown("### Target Sign Selection")
            
            cat_opts = ["Alphabet Letters (Aâ€“Z)", "Core ISL Gestures", "Custom Label"]
            cat_default_idx = 0
            if st.session_state.target_category in cat_opts:
                cat_default_idx = cat_opts.index(st.session_state.target_category)
    
            vocab_cat = st.radio(
                "Category",
                cat_opts,
                index=cat_default_idx,
                horizontal=True,
                key="studio_vocab_cat_radio"
            )
            st.session_state.target_category = vocab_cat
    
            counts_dict = dataset_mgr.get_class_counts()
            active_model_classes = set(predictor.classes) if predictor.is_loaded else set()
    
            if vocab_cat == "Alphabet Letters (Aâ€“Z)":
                default_let_idx = 0
                if st.session_state.target_letter in ISL_ALPHABET_LETTERS:
                    default_let_idx = ISL_ALPHABET_LETTERS.index(st.session_state.target_letter)
    
                opts = []
                for l in ISL_ALPHABET_LETTERS:
                    cnt = counts_dict.get(l, 0)
                    if l in active_model_classes:
                        st_txt = "Active"
                    elif cnt > 0:
                        st_txt = "Ready to train"
                    else:
                        st_txt = "Needs data"
                    opts.append(f"{l} â€” {st_txt} ({cnt} samples)")
    
                sel_idx = st.selectbox(
                    "Select Target Letter (Aâ€“Z)",
                    range(len(ISL_ALPHABET_LETTERS)),
                    index=default_let_idx,
                    format_func=lambda i: opts[i],
                    key="studio_target_letter_select"
                )
                target_sign = ISL_ALPHABET_LETTERS[sel_idx]
                st.session_state.target_letter = target_sign
    
            elif vocab_cat == "Core ISL Gestures":
                opts = []
                for g in CORE_ISL_GESTURES:
                    cnt = counts_dict.get(g, 0)
                    st_txt = "Active" if g in active_model_classes else ("Ready" if cnt > 0 else "Needs data")
                    opts.append(f"{g} â€” {st_txt} ({cnt} samples)")
    
                sel_idx = st.selectbox(
                    "Select Core Gesture",
                    range(len(CORE_ISL_GESTURES)),
                    format_func=lambda i: opts[i],
                    key="studio_core_gesture_select"
                )
                target_sign = CORE_ISL_GESTURES[sel_idx]
            else:
                target_sign = st.text_input("Custom Sign Label:").strip().upper()
    
            sample_count = counts_dict.get(target_sign, 0)
    
            # Prominent Letter / Sign Display Card with ISL Posture Guidance
            guide_info = ISL_ALPHABET_GUIDE.get(target_sign, None)
            
            if target_sign in active_model_classes:
                status_badge = "<span class='sb-matrix-badge-active' style='font-size:0.75rem; padding:3px 7px;'>â— Active in Classifier</span>"
            elif sample_count > 0:
                status_badge = f"<span class='sb-matrix-badge-ready' style='font-size:0.75rem; padding:3px 7px;'>â–² Ready to Train ({sample_count} samples)</span>"
            else:
                status_badge = "<span class='sb-matrix-badge-needs' style='font-size:0.75rem; padding:3px 7px;'>â—‹ Needs Data (0 samples)</span>"
    
            motion_alert = ""
            if guide_info and "motion" in guide_info and "Note" in guide_info["motion"]:
                motion_alert = f"<div style='font-size:0.8rem; color:var(--sb-warning); background:var(--sb-warning-bg); padding:6px 10px; border-radius:4px; border:1px solid var(--sb-warning-border); margin-top:0.4rem;'>âš ï¸ <strong>Movement Note:</strong> {guide_info['motion']}</div>"
    
            st.markdown(
                f"""
                <div class="sb-callout" style="margin-top:1rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                        <span style="font-size:2.5rem; font-weight:800; color:var(--sb-primary); font-family:'JetBrains Mono',monospace;">{target_sign}</span>
                        <div>{status_badge}</div>
                    </div>
                    <div style="font-size:0.88rem; color:var(--sb-text-main); font-weight:600; margin-bottom:0.25rem;">
                        ISL Posture Guide:
                    </div>
                    <div style="font-size:0.85rem; color:var(--sb-text-muted); line-height:1.5; margin-bottom:0.6rem;">
                        {guide_info['posture'] if guide_info else 'Maintain the verified static hand posture for this sign.'}
                    </div>
                    <div style="font-size:0.82rem; color:var(--sb-primary); background:var(--sb-primary-light); padding:6px 10px; border-radius:4px; border:1px solid var(--sb-primary-border);">
                        ðŸ’¡ <strong>Camera Guidance:</strong> {guide_info['tips'] if guide_info else 'Keep hand clearly visible in the center of the webcam frame.'}
                    </div>
                    {motion_alert}
                </div>
                """,
                unsafe_allow_html=True,
            )
    
            # Metadata settings
            st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
            c_sess1, c_sess2 = st.columns(2)
            with c_sess1:
                sess_id = st.text_input("Session ID", value=f"session_{datetime.now().strftime('%m%d_%H%M')}")
            with c_sess2:
                user_id = st.text_input("Signer ID", value="signer_1")
    
            # Data Management (Deletion with Confirmation)
            st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
            with st.expander(f"Manage Data for '{target_sign}'"):
                st.write(f"Current sample count for **`{target_sign}`**: **{sample_count}**")
                confirm_del = st.checkbox(
                    f"I confirm that I want to delete all {sample_count} samples for '{target_sign}'.",
                    key=f"confirm_del_box_{target_sign}",
                )
                if st.button(f"Delete All '{target_sign}' Samples", type="secondary", disabled=not (confirm_del and sample_count > 0), key=f"btn_del_{target_sign}"):
                    del_n = dataset_mgr.delete_samples_for_label(target_sign)
                    st.success(f"Deleted {del_n} samples for '{target_sign}'.")
                    time.sleep(0.4)
                    st.rerun()
    
        with col_d_right:
            st.markdown("### Webcam Data Recorder")
            st.markdown(
                """
                <div style="font-size:0.84rem; color:var(--sb-text-muted); margin-bottom:0.8rem;">
                    Hold the hand posture steadily facing the camera. 21 joints are tracked via MediaPipe. Empty frames without a detected hand are automatically rejected.
                </div>
                """,
                unsafe_allow_html=True,
            )
    
            c_ctrl1, c_ctrl2, c_ctrl3 = st.columns([1.2, 1, 1])
            with c_ctrl1:
                c_burst = st.button("Capture 10 Samples (Burst)", type="primary", use_container_width=True, key="d_burst")
            with c_ctrl2:
                c_single = st.button("Capture 1 Sample", use_container_width=True, key="d_single")
            with c_ctrl3:
                c_preview = st.toggle("Camera Preview", value=False, key="d_open")
    
            cap_holder = st.empty()
            recorder_status = st.empty()
    
            # 1. Burst Capture (10 samples)
            if c_burst:
                if not target_sign:
                    st.warning("Please specify a target sign label before recording.")
                else:
                    with st.spinner(f"Opening camera to capture 10 samples for '{target_sign}'..."):
                        cap_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                        if not cap_capture.isOpened():
                            cap_capture = cv2.VideoCapture(0)
                        if not cap_capture.isOpened():
                            cap_capture = cv2.VideoCapture(1)
    
                        if not cap_capture.isOpened():
                            recorder_status.error("Could not access webcam for data capture. Check camera permissions.")
                        else:
                            cap_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                            collected_samples = []
                            attempts = 0
                            p_bar = st.progress(0, text=f"Capturing samples for {target_sign}...")
    
                            while len(collected_samples) < 10 and attempts < 70:
                                attempts += 1
                                r_f, f_raw = cap_capture.read()
                                if r_f:
                                    f_mir = cv2.flip(f_raw, 1)
                                    d_res = tracker.detect(f_mir)
                                    ann_f = tracker.draw_landmarks(f_mir, d_res)
                                    cap_holder.image(cv2.cvtColor(ann_f, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
    
                                    if d_res.has_hand and d_res.hands:
                                        f_vec = preprocessor.extract_from_landmarks(d_res.hands[0].landmarks)
                                        if f_vec is not None:
                                            collected_samples.append((target_sign, f_vec, sess_id, user_id, "Right"))
                                            p_bar.progress(len(collected_samples) / 10.0, text=f"Captured {len(collected_samples)}/10 samples...")
                                time.sleep(0.12)
    
                            cap_capture.release()
                            if collected_samples:
                                added_n = dataset_mgr.append_samples_batch(collected_samples)
                                st.success(f"Successfully recorded and saved {added_n} samples for '{target_sign}'!")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                recorder_status.warning("No hand detected during capture attempts. Ensure your hand is clearly visible.")
    
            # 2. Single Sample Capture
            elif c_single:
                if not target_sign:
                    st.warning("Please specify a target sign label before recording.")
                else:
                    with st.spinner(f"Capturing single sample for '{target_sign}'..."):
                        cap_s = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                        if not cap_s.isOpened():
                            cap_s = cv2.VideoCapture(0)
                        if cap_s.isOpened():
                            cap_s.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap_s.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                            ret_s, f_raw = cap_s.read()
                            cap_s.release()
                            if ret_s:
                                f_mir = cv2.flip(f_raw, 1)
                                d_res = tracker.detect(f_mir)
                                ann_f = tracker.draw_landmarks(f_mir, d_res)
                                cap_holder.image(cv2.cvtColor(ann_f, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
                                if d_res.has_hand and d_res.hands:
                                    f_vec = preprocessor.extract_from_landmarks(d_res.hands[0].landmarks)
                                    if f_vec is not None:
                                        dataset_mgr.append_sample(target_sign, f_vec, sess_id, user_id, "Right")
                                        st.success(f"Saved 1 sample for '{target_sign}'!")
                                        time.sleep(0.4)
                                        st.rerun()
                                else:
                                    recorder_status.warning("No hand detected. Sample was rejected.")
                        else:
                            recorder_status.error("Could not access webcam.")
    
            # 3. Static Live Camera Preview
            elif c_preview:
                cap_d = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not cap_d.isOpened():
                    cap_d = cv2.VideoCapture(0)
                if cap_d.isOpened():
                    ret_d, frame_d = cap_d.read()
                    if ret_d:
                        frame_d = cv2.flip(frame_d, 1)
                        det_d = tracker.detect(frame_d)
                        annotated_d = tracker.draw_landmarks(frame_d, det_d)
                        cap_holder.image(cv2.cvtColor(annotated_d, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
                    cap_d.release()
    
            # Protocol guidance alert
            st.markdown(
                """
                <div class="sb-callout" style="margin-top:1.2rem;">
                    <div class="sb-callout-title">
                        Recommended Data Collection Protocol
                    </div>
                    <ul style="font-size:0.82rem; color:var(--sb-text-muted); margin:0; padding-left:1.2rem; line-height:1.55;">
                        <li><strong>Vary Distance:</strong> Capture some samples close (~35 cm) and some further (~65 cm).</li>
                        <li><strong>Vary Hand Position:</strong> Shift hand slightly left, center, right, and vertically.</li>
                        <li><strong>Vary Angle:</strong> Tilt hand slightly (Â±15Â°) to ensure rotation invariance.</li>
                        <li><strong>Lighting & Background:</strong> Collect samples across different ambient lighting.</li>
                        <li><strong>Minimum Recommendation:</strong> Collect at least 15â€“20 samples per letter for balanced training.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    # Sub-Tab 2: Model Training & Evaluation
    with tab_train:
        st.markdown("### Random Forest Classifier Training Pipeline")
        st.markdown(
            """
            <div style="font-size:0.85rem; color:var(--sb-text-muted); margin-bottom:1rem;">
                Train a balanced Random Forest model on your locally recorded samples. Evaluated with <code>GroupShuffleSplit</code> across session IDs to ensure zero data leakage.
            </div>
            """,
            unsafe_allow_html=True,
        )
    
        is_valid, validation_issues = dataset_mgr.validate_dataset()
        if not is_valid:
            st.warning("âš ï¸ **Dataset Validation Alert:**")
            for issue in validation_issues:
                st.markdown(f"- {issue}")
            st.info("Collect samples for at least 2 distinct classes in **Tab 1: Dataset Collection** before training.")
        else:
            st.success("Dataset meets minimum requirements for model training.")
    
        t1, t2 = st.columns(2)
        with t1:
            n_trees_opt = st.slider("Trees in Forest", 50, 300, 150, 25)
        with t2:
            test_ratio_opt = st.slider("Test Split Ratio", 0.15, 0.35, 0.20, 0.05)
    
        can_train = len(class_counts) >= 2 and total_samples >= 10
        if st.button("Train Model Classifier", type="primary", use_container_width=True, disabled=not can_train, key="train_btn"):
            with st.spinner("Training Random Forest with session-based cross-validation..."):
                try:
                    trainer = ModelTrainer(n_estimators=n_trees_opt)
                    res = trainer.train_and_evaluate(test_size=test_ratio_opt)
                    predictor.load_model(res["model_path"])
    
                    st.success(f"Model successfully trained and saved to `{res['model_path']}`!")
                    st.info(f"**Active Recognized Classes ({len(res['classes'])}):** {', '.join(res['classes'])}")
    
                    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                    with m_col1:
                        st.metric("Test Accuracy", f"{res['accuracy'] * 100:.1f}%")
                    with m_col2:
                        st.metric("Precision (Macro)", f"{res['precision_macro'] * 100:.1f}%")
                    with m_col3:
                        st.metric("Recall (Macro)", f"{res['recall_macro'] * 100:.1f}%")
                    with m_col4:
                        st.metric("F1 Score (Macro)", f"{res['f1_macro'] * 100:.1f}%")
    
                    st.markdown("#### Confusion Matrix Heatmap")
                    fig_cm = trainer.render_confusion_matrix_plot(res["confusion_matrix"], res["classes"])
                    st.pyplot(fig_cm)
    
                    if st.button("Test Model in Live App â†’", type="primary", key="train_go_live_btn"):
                        st.session_state.active_page = "Live App"
                        st.rerun()
    
                except Exception as ex:
                    st.error(f"Training failed: {ex}")
    
    
