"""
Studio page for SignBridge: Dataset Collection, Model Training, and Custom Commands.
Enables collecting labeled hand landmarks, viewing alphabet coverage, training local
Random Forest models, and managing custom gesture commands and macro actions.
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
from backend.text_to_speech import speak_pyttsx3
from frontend.utils.command_manager import CustomCommandManager


def render_studio_page(
    dataset_mgr: DatasetManager,
    preprocessor: LandmarkPreprocessor,
    tracker: HandTracker,
    predictor: SignPredictor,
) -> None:
    """Renders the dataset collection, model training, and custom commands studio interface."""
    st.markdown(
        """
        <div class="sb-section-tag">// MLOPS, DATASET & COMMAND STUDIO</div>
        <h1 class="sb-section-heading">SignBridge Studio</h1>
        <p class="sb-section-desc">
            Collect verified hand landmark coordinates, evaluate dataset integrity, train local Random Forest models, and configure personal gesture commands.
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    class_counts = dataset_mgr.get_class_counts()
    total_samples = sum(class_counts.values())
    cmd_mgr = CustomCommandManager()

    tab_data, tab_train, tab_cmd = st.tabs([
        "1. Dataset Collection (A–Z & Gestures)",
        "2. Model Training & Evaluation",
        "3. Custom Manual Commands & Macro Actions",
    ])
    
    # =========================================================================
    # Sub-Tab 1: Dataset Collection
    # =========================================================================
    with tab_data:
        col_d_left, col_d_right = st.columns([1.1, 1.4], gap="large")

        with col_d_left:
            st.markdown("### Target Sign Selection")

            cat_opts = ["Alphabet Letters (A–Z)", "Core ISL Gestures", "Custom Label"]
            cat_default_idx = 0
            if st.session_state.get("target_category") in cat_opts:
                cat_default_idx = cat_opts.index(st.session_state.target_category)

            vocab_cat = st.radio(
                "Category",
                cat_opts,
                index=cat_default_idx,
                horizontal=True,
                key="studio_vocab_cat_radio",
            )
            st.session_state.target_category = vocab_cat

            counts_dict = class_counts
            active_model_classes = set(predictor.classes) if predictor.is_loaded else set()

            if vocab_cat == "Alphabet Letters (A–Z)":
                if st.session_state.get("target_letter") not in ISL_ALPHABET_LETTERS:
                    st.session_state.target_letter = "A"

                if "studio_target_letter_select" not in st.session_state or st.session_state["studio_target_letter_select"] not in ISL_ALPHABET_LETTERS:
                    st.session_state["studio_target_letter_select"] = st.session_state.target_letter

                def _on_studio_target_letter_change():
                    new_val = st.session_state.get("studio_target_letter_select")
                    if new_val in ISL_ALPHABET_LETTERS:
                        st.session_state.target_letter = new_val

                curr_letter = st.session_state["studio_target_letter_select"]
                curr_idx = ISL_ALPHABET_LETTERS.index(curr_letter) if curr_letter in ISL_ALPHABET_LETTERS else 0

                def _fmt_letter(l: str) -> str:
                    cnt = counts_dict.get(l, 0)
                    if l in active_model_classes:
                        st_txt = "Active"
                    elif cnt > 0:
                        st_txt = "Ready to train"
                    else:
                        st_txt = "Needs data"
                    return f"{l} — {st_txt} ({cnt} samples)"

                sel_letter = st.selectbox(
                    "Select Target Letter (A–Z)",
                    options=ISL_ALPHABET_LETTERS,
                    index=curr_idx,
                    format_func=_fmt_letter,
                    key="studio_target_letter_select",
                    on_change=_on_studio_target_letter_change,
                )
                target_sign = sel_letter
                st.session_state.target_letter = target_sign

            elif vocab_cat == "Core ISL Gestures":
                if st.session_state.get("studio_core_gesture_select") not in CORE_ISL_GESTURES:
                    st.session_state["studio_core_gesture_select"] = CORE_ISL_GESTURES[0]

                def _on_core_gesture_change():
                    new_g = st.session_state.get("studio_core_gesture_select")
                    if new_g in CORE_ISL_GESTURES:
                        st.session_state.target_gesture = new_g

                curr_g = st.session_state["studio_core_gesture_select"]
                curr_g_idx = CORE_ISL_GESTURES.index(curr_g) if curr_g in CORE_ISL_GESTURES else 0

                def _fmt_gesture(g: str) -> str:
                    cnt = counts_dict.get(g, 0)
                    st_txt = "Active" if g in active_model_classes else ("Ready" if cnt > 0 else "Needs data")
                    return f"{g} — {st_txt} ({cnt} samples)"

                sel_gesture = st.selectbox(
                    "Select Core Gesture",
                    options=CORE_ISL_GESTURES,
                    index=curr_g_idx,
                    format_func=_fmt_gesture,
                    key="studio_core_gesture_select",
                    on_change=_on_core_gesture_change,
                )
                target_sign = sel_gesture
            else:
                target_sign = st.text_input("Custom Sign Label:", key="studio_custom_label_input").strip().upper()

            sample_count = counts_dict.get(target_sign, 0) if target_sign else 0

            # Prominent Letter / Sign Display Card with ISL Posture Guidance
            guide_info = ISL_ALPHABET_GUIDE.get(target_sign, None) if target_sign else None

            if not target_sign:
                status_badge = "<span class='sb-matrix-badge-needs' style='font-size:0.75rem; padding:3px 7px;'>⚠️ No Label Specified</span>"
            elif target_sign in active_model_classes:
                status_badge = "<span class='sb-matrix-badge-active' style='font-size:0.75rem; padding:3px 7px;'>● Active in Classifier</span>"
            elif sample_count > 0:
                status_badge = f"<span class='sb-matrix-badge-ready' style='font-size:0.75rem; padding:3px 7px;'>▲ Ready to Train ({sample_count} samples)</span>"
            else:
                status_badge = "<span class='sb-matrix-badge-needs' style='font-size:0.75rem; padding:3px 7px;'>○ Needs Data (0 samples)</span>"

            motion_alert = ""
            if guide_info and "motion" in guide_info and "Note" in guide_info["motion"]:
                motion_alert = f"<div style='font-size:0.8rem; color:var(--sb-warning); background:var(--sb-warning-bg); padding:6px 10px; border-radius:6px; border:1px solid var(--sb-warning-border); margin-top:0.4rem;'>⚠️ <strong>Movement Note:</strong> {guide_info['motion']}</div>"

            display_heading = target_sign if target_sign else "—"
            st.markdown(
                f"""
                <div class="sb-callout" style="margin-top:1rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                        <span style="font-size:2.5rem; font-weight:800; color:var(--sb-primary-hover); font-family:'JetBrains Mono',monospace;">{display_heading}</span>
                        <div>{status_badge}</div>
                    </div>
                    <div style="font-size:0.88rem; color:var(--sb-text-main); font-weight:600; margin-bottom:0.25rem;">
                        ISL Posture Guide:
                    </div>
                    <div style="font-size:0.85rem; color:var(--sb-text-muted); line-height:1.5; margin-bottom:0.6rem;">
                        {guide_info['posture'] if guide_info else ('Maintain the verified static hand posture for this sign.' if target_sign else 'Please select an alphabet letter or enter a custom label.')}
                    </div>
                    <div style="font-size:0.82rem; color:var(--sb-primary-hover); background:var(--sb-primary-light); padding:8px 12px; border-radius:6px; border:1px solid var(--sb-primary-border);">
                        💡 <strong>Camera Guidance:</strong> {guide_info['tips'] if guide_info else ('Keep hand clearly visible in the center of the webcam frame.' if target_sign else 'Camera recording will be enabled once a valid sign is chosen.')}
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
            with st.expander(f"Manage Data for '{target_sign}'" if target_sign else "Manage Data"):
                st.write(f"Current sample count for **`{target_sign}`**: **{sample_count}**")
                confirm_del = st.checkbox(
                    f"I confirm that I want to delete all {sample_count} samples for '{target_sign}'.",
                    key=f"confirm_del_box_{target_sign}",
                    disabled=not bool(target_sign and sample_count > 0),
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

            # Prominently display active target sign near recorder controls
            if target_sign:
                st.markdown(
                    f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; background:var(--sb-surface-muted); border:1px solid var(--sb-border); border-left:4px solid var(--sb-primary); border-radius:8px; padding:0.75rem 1rem; margin-bottom:0.85rem;">
                        <div>
                            <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle);">Active Recording Label</div>
                            <div style="font-size:1.55rem; font-weight:800; color:var(--sb-primary-hover); font-family:'JetBrains Mono',monospace;">{target_sign}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--sb-text-subtle);">Samples in Dataset</div>
                            <div style="font-size:1.25rem; font-weight:700; color:var(--sb-text-main); font-family:'JetBrains Mono',monospace;">{sample_count}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.warning("⚠️ No target sign selected. Please select an alphabet letter or enter a custom label before recording.")

            c_ctrl1, c_ctrl2, c_ctrl3 = st.columns([1.2, 1, 1])
            with c_ctrl1:
                c_burst = st.button("Capture 10 Samples (Burst)", type="primary", use_container_width=True, key="d_burst", disabled=not bool(target_sign))
            with c_ctrl2:
                c_single = st.button("Capture 1 Sample", use_container_width=True, key="d_single", disabled=not bool(target_sign))
            with c_ctrl3:
                c_preview = st.toggle("Camera Preview", value=False, key="d_open")

            cap_holder = st.empty()
            recorder_status = st.empty()

            # Notification banner if samples were recorded in previous run
            if "last_recorded_target" in st.session_state:
                just_saved_target = st.session_state.pop("last_recorded_target")
                just_saved_count = st.session_state.pop("last_recorded_count", 0)
                tot_for_target = counts_dict.get(just_saved_target, 0)
                recorder_status.success(f"✅ Successfully saved {just_saved_count} sample(s) labeled as **`{just_saved_target}`** (Total in dataset: **{tot_for_target}**).")

            # 1. Burst Capture (10 samples)
            if c_burst:
                if not target_sign:
                    recorder_status.error("⚠️ Cannot record: no sign label is selected. Please choose a letter first.")
                else:
                    active_label_to_save = target_sign
                    with st.spinner(f"Opening camera to capture 10 samples for '{active_label_to_save}'..."):
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
                            p_bar = st.progress(0, text=f"Capturing samples for '{active_label_to_save}'...")

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
                                            collected_samples.append((active_label_to_save, f_vec, sess_id, user_id, "Right"))
                                            p_bar.progress(len(collected_samples) / 10.0, text=f"Captured {len(collected_samples)}/10 samples for '{active_label_to_save}'...")
                                time.sleep(0.12)

                            cap_capture.release()
                            if collected_samples:
                                added_n = dataset_mgr.append_samples_batch(collected_samples)
                                st.session_state.last_recorded_target = active_label_to_save
                                st.session_state.last_recorded_count = added_n
                                time.sleep(0.3)
                                st.rerun()
                            else:
                                recorder_status.warning("No hand detected during capture attempts. Ensure your hand is clearly visible.")

            # 2. Single Sample Capture
            elif c_single:
                if not target_sign:
                    recorder_status.error("⚠️ Cannot record: no sign label is selected. Please choose a letter first.")
                else:
                    active_label_to_save = target_sign
                    with st.spinner(f"Capturing single sample for '{active_label_to_save}'..."):
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
                                        dataset_mgr.append_sample(active_label_to_save, f_vec, sess_id, user_id, "Right")
                                        st.session_state.last_recorded_target = active_label_to_save
                                        st.session_state.last_recorded_count = 1
                                        time.sleep(0.3)
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
                        <li><strong>Vary Angle:</strong> Tilt hand slightly (±15°) to ensure rotation invariance.</li>
                        <li><strong>Lighting & Background:</strong> Collect samples across different ambient lighting.</li>
                        <li><strong>Minimum Recommendation:</strong> Collect at least 15–20 samples per letter for balanced training.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    # =========================================================================
    # Sub-Tab 2: Model Training & Evaluation
    # =========================================================================
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
            st.warning("⚠️ **Dataset Validation Alert:**")
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
    
                    if st.button("Test Model in Live App →", type="primary", key="train_go_live_btn"):
                        st.session_state.active_page = "Live App"
                        st.rerun()
    
                except Exception as ex:
                    st.error(f"Training failed: {ex}")

    # =========================================================================
    # Sub-Tab 3: Custom Manual Commands & Macro Actions
    # =========================================================================
    with tab_cmd:
        st.markdown(
            """
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:1rem;">
                <div>
                    <h3 style="margin:0; font-size:1.35rem; color:var(--sb-text-main);">Personal Gesture Automation & Macro Actions</h3>
                    <div style="font-size:0.86rem; color:var(--sb-text-muted); margin-top:0.25rem;">
                        Assign custom spoken phrases, emergency calls, or multi-lingual actions triggered whenever a specific sign is recognized.
                    </div>
                </div>
                <div class="sb-status-chip">
                    <span class="sb-status-dot sb-dot-active"></span>
                    <span>LOCAL JSON STORAGE</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        all_commands = cmd_mgr.load_commands()
        active_cmd_count = sum(1 for c in all_commands if c.get("enabled", True))

        # Metrics overview bar
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            st.metric("Total Configured Macros", len(all_commands))
        with c_m2:
            st.metric("Active & Armed", active_cmd_count)
        with c_m3:
            st.metric("Storage Engine", "Local JSON (Private)")

        st.markdown("<hr style='margin:1.25rem 0;'>", unsafe_allow_html=True)

        col_cmd_list, col_cmd_new = st.columns([1.35, 1], gap="large")

        with col_cmd_list:
            st.markdown("### Configured Commands")
            if not all_commands:
                st.info("No custom commands currently configured. Use the form on the right to create your first gesture macro.")
            else:
                for cmd in all_commands:
                    cmd_id = cmd.get("id")
                    cmd_name = cmd.get("name", "Unnamed Command")
                    trigger = cmd.get("trigger", "—")
                    act_type = cmd.get("action_type", "Vocalize Speech")
                    payload = cmd.get("payload", "")
                    enabled = cmd.get("enabled", True)
                    desc = cmd.get("description", "")

                    status_dot = "sb-dot-ready" if enabled else "sb-dot-neutral"
                    status_text = "ARMED // ACTIVE" if enabled else "DISABLED"

                    st.markdown(
                        f"""
                        <div class="sb-command-card">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.6rem;">
                                <div>
                                    <div style="font-size:1.1rem; font-weight:700; color:var(--sb-text-main);">{cmd_name}</div>
                                    <div style="font-size:0.8rem; color:var(--sb-text-muted); margin-top:2px;">{desc}</div>
                                </div>
                                <div class="sb-status-chip" style="font-size:0.68rem; padding:2px 8px;">
                                    <span class="sb-status-dot {status_dot}"></span>
                                    <span>{status_text}</span>
                                </div>
                            </div>
                            <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:0.75rem;">
                                <span class="sb-brand-badge" style="background:rgba(99,102,241,0.18); color:#818cf8; border-color:rgba(99,102,241,0.35);">
                                    ⚡ TRIGGER: {trigger}
                                </span>
                                <span class="sb-brand-badge" style="background:rgba(6,182,212,0.15); color:#06b6d4; border-color:rgba(6,182,212,0.3);">
                                    {act_type}
                                </span>
                            </div>
                            <div style="background:rgba(8,11,20,0.8); border:1px solid var(--sb-border); border-radius:6px; padding:0.6rem 0.85rem; font-family:'JetBrains Mono',monospace; font-size:0.82rem; color:var(--sb-text-main); margin-bottom:0.85rem;">
                                💬 "{payload}"
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Command card action buttons
                    btn_c1, btn_c2, btn_c3 = st.columns([1.1, 1.1, 1.2])
                    with btn_c1:
                        if st.button("🔊 Test Voice", key=f"test_cmd_{cmd_id}", use_container_width=True):
                            speak_pyttsx3(payload)
                            st.toast(f"Executed: \"{payload}\"", icon="🔊")
                    with btn_c2:
                        toggle_lbl = "Disable" if enabled else "Enable"
                        if st.button(toggle_lbl, key=f"toggle_cmd_{cmd_id}", use_container_width=True):
                            cmd_mgr.toggle_command(cmd_id)
                            st.rerun()
                    with btn_c3:
                        with st.popover("Delete"):
                            st.write(f"Delete **'{cmd_name}'**?")
                            if st.button("Confirm Delete", key=f"del_confirm_{cmd_id}", type="primary", use_container_width=True):
                                cmd_mgr.delete_command(cmd_id)
                                st.rerun()

                    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

        with col_cmd_new:
            st.markdown("### Create New Gesture Command")
            st.markdown(
                """
                <div style="font-size:0.84rem; color:var(--sb-text-muted); margin-bottom:1rem;">
                    Link a recognized hand sign to an immediate verbal sentence or emergency notification.
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.form("create_custom_command_form", clear_on_submit=True):
                new_name = st.text_input("Command Name", placeholder="e.g. Call for Water or Medical Alert")

                # Select trigger sign: core gestures first, then alphabet letters
                trigger_options = CORE_ISL_GESTURES + ISL_ALPHABET_LETTERS
                new_trigger = st.selectbox(
                    "Trigger Sign Gesture or Letter",
                    options=trigger_options,
                    index=0,
                    help="When this gesture is recognized with high confidence, the action will be triggered.",
                )

                new_action = st.selectbox(
                    "Macro Action Type",
                    options=[
                        "Vocalize Speech",
                        "Translate to Hindi & Speak",
                        "Emergency Alarm & Vocalize",
                        "Insert Custom Sentence",
                    ],
                    index=0,
                )

                new_payload = st.text_area(
                    "Spoken Message / Text Response",
                    placeholder="Enter the full sentence to vocalize (e.g. 'Excuse me, could you please give me a glass of water?')...",
                    height=95,
                )

                new_desc = st.text_input(
                    "Description (Optional)",
                    placeholder="e.g. Asks for drinking water in public settings",
                )

                create_submitted = st.form_submit_button("Create Custom Command ⚡", type="primary", use_container_width=True)
                if create_submitted:
                    success, msg = cmd_mgr.add_command(
                        name=new_name,
                        trigger=new_trigger,
                        action_type=new_action,
                        payload=new_payload,
                        description=new_desc,
                        enabled=True,
                    )
                    if success:
                        st.success(msg)
                        time.sleep(0.4)
                        st.rerun()
                    else:
                        st.error(msg)
