# SignBridge — Autonomous Engineering & Project Rules

## 1. Autonomous Operation Guidelines
- **Autonomous Execution**: Work end-to-end on routine development, bug fixes, refactoring, and UI improvements without seeking repeated confirmations for standard actions (inspecting files, reading code, editing project files, running builds, executing tests).
- **Self-Directed Problem Solving**: When encountering errors or build/test failures, inspect terminal logs, diagnose root causes, and iterate through reasonable alternatives autonomously.
- **Sensible Implementation Decisions**: Make sound engineering and design decisions consistent with the project's architecture rather than pausing for minor details.
- **End-to-End Task Completion**: Complete requested features and fixes fully before presenting results. Avoid stopping mid-task to ask for permission to continue.

## 2. Project Architecture & Preferences
- **Project**: SignBridge — Sign Language Recognition Assistant.
- **Environment**: Windows 11, PowerShell, Python 3.11 virtual environment (`.\.venv\Scripts\python.exe`).
- **Core Functionality Preservation**:
  - **Machine Learning**: Maintain the 21-landmark tracking pipeline (MediaPipe Tasks HandLandmarker) and 63-feature translation/scale-invariant normalization (`src/preprocessing.py`).
  - **Model**: Retain the trained Random Forest classifier (`models/gesture_model.joblib`) unless model retraining or dataset changes are explicitly requested.
  - **Sentence Composition**: Preserve the debounced sentence builder and fingerspelling assembly (`src/text_to_speech.py`).
  - **Offline Translation**: Maintain local neural translation via MarianMT (`src/translator.py` and `models/opus_mt_en_hi`). Never substitute with cloud APIs.
  - **UI Entry Point**: The primary application entry point is `app.py`. Maintain high-contrast accessible design, dark/light theme switching, and anti-stale Streamlit styling.
- **Surgical Edits**: Prefer minimal, reliable, and targeted edits over broad rewrites.
- **Verification Rule**: Always verify code changes with:
  1. `.\.venv\Scripts\python.exe -m py_compile <modified_file>`
  2. `.\.venv\Scripts\pytest.exe -v`
  Do not state that changes or features work without running verification tests.

## 3. Tool & Command Permissions
- Execute routine development commands (`pytest`, `py_compile`, `streamlit run`, `pip install` when needed) directly.
- If a command is restricted or blocked by approval mechanisms, explain the exact constraint and pivot to an available permitted alternative.

## 4. Safety & Security Safeguards
- Do not bypass platform security policies or disable mandatory safety controls.
- Do not delete critical directories, overwrite unrelated files, or expose credentials/secrets.
- Do not publish code or send private data to external endpoints.

## 5. Reporting Contract
Upon task completion, provide a concise summary containing:
1. What was changed and why.
2. Exact files modified.
3. Automated test runs and verification results.
4. Genuine blockers or architectural decisions that require user input (if any).

