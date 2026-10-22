"""
SignBridge — Premium Dark Tech & AI Intelligence Design System.
Defines dynamic CSS tokens, typography, glassmorphism panels, glowing accents,
status indicators, and accessible overrides for Streamlit.
"""

def get_theme_css(theme: str) -> str:
    """Generate dynamic CSS tokens and Streamlit component overrides based on theme."""
    is_dark = (theme == "dark")
    if is_dark:
        color_scheme = "dark"
        vars_css = """
        color-scheme: dark;
        --background-color: var(--sb-bg);
        --secondary-background-color: #0f172a;
        --text-color: var(--sb-text-main);
        --primary-color: #6366f1;
        --sb-bg: #0c0d10;
        --sb-canvas: #080b14;
        --sb-surface: #0f172a;
        --sb-surface-muted: #131c31;
        --sb-surface-highlight: #1e293b;
        --sb-border: rgba(99, 102, 241, 0.22);
        --sb-border-subtle: rgba(255, 255, 255, 0.08);
        --sb-border-strong: rgba(99, 102, 241, 0.45);
        --sb-text-main: #f4f5f8;
        --sb-text-white: #ffffff;
        --sb-text-muted: #94a3b8;
        --sb-text-subtle: #64748b;
        --sb-primary: #6366f1;
        --sb-primary-hover: #818cf8;
        --sb-primary-light: rgba(99, 102, 241, 0.14);
        --sb-primary-border: rgba(99, 102, 241, 0.38);
        --sb-secondary: #06b6d4;
        --sb-secondary-hover: #38bdf8;
        --sb-secondary-light: rgba(6, 182, 212, 0.14);
        --sb-success: #10b981;
        --sb-success-bg: rgba(16, 185, 129, 0.14);
        --sb-success-border: rgba(16, 185, 129, 0.35);
        --sb-warning: #f59e0b;
        --sb-warning-bg: rgba(245, 158, 11, 0.14);
        --sb-warning-border: rgba(245, 158, 11, 0.35);
        --sb-error: #ef4444;
        --sb-chip-bg: #131c31;
        --sb-btn-bg: #6366f1;
        --sb-btn-text: #ffffff;
        --sb-radius-card: 14px;
        --sb-radius-btn: 8px;
        --sb-radius-badge: 999px;
        --sb-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.4);
        --sb-shadow-md: 0 4px 16px -2px rgba(0, 0, 0, 0.5), 0 0 16px rgba(99, 102, 241, 0.08);
        --sb-shadow-lg: 0 16px 32px -4px rgba(0, 0, 0, 0.7), 0 0 28px rgba(99, 102, 241, 0.12);
        --sb-radial-glow: radial-gradient(circle at 50% -20%, rgba(99, 102, 241, 0.22) 0%, rgba(6, 182, 212, 0.08) 45%, rgba(8, 11, 20, 0) 75%);
        --sb-heading-gradient: linear-gradient(135deg, #ffffff 40%, #94a3b8 100%);
        --sb-brand-gradient: linear-gradient(135deg, #ffffff 30%, #cbd5e1 100%);
        --sb-metric-gradient: linear-gradient(135deg, #ffffff 40%, #818cf8 100%);
        """
    else:
        color_scheme = "light"
        vars_css = """
        color-scheme: light;
        --background-color: var(--sb-bg);
        --secondary-background-color: #f1f5f9;
        --text-color: var(--sb-text-main);
        --primary-color: #4f46e5;
        --sb-bg: #fbfaf8;
        --sb-canvas: #f8fafc;
        --sb-surface: #ffffff;
        --sb-surface-muted: #f1f5f9;
        --sb-surface-highlight: #e2e8f0;
        --sb-border: #e2e8f0;
        --sb-border-subtle: #f1f5f9;
        --sb-border-strong: #cbd5e1;
        --sb-text-main: #141517;
        --sb-text-white: #0f172a;
        --sb-text-muted: #475569;
        --sb-text-subtle: #64748b;
        --sb-primary: #4f46e5;
        --sb-primary-hover: #4338ca;
        --sb-primary-light: #eef2ff;
        --sb-primary-border: #c7d2fe;
        --sb-secondary: #0891b2;
        --sb-secondary-hover: #0e7490;
        --sb-secondary-light: #ecfeff;
        --sb-success: #059669;
        --sb-success-bg: #ecfdf5;
        --sb-success-border: #a7f3d0;
        --sb-warning: #d97706;
        --sb-warning-bg: #fffbeb;
        --sb-warning-border: #fde68a;
        --sb-error: #dc2626;
        --sb-chip-bg: #f1f5f9;
        --sb-btn-bg: #4f46e5;
        --sb-btn-text: #ffffff;
        --sb-radius-card: 14px;
        --sb-radius-btn: 8px;
        --sb-radius-badge: 999px;
        --sb-shadow: 0 1px 3px 0 rgba(16, 24, 40, 0.05);
        --sb-shadow-md: 0 4px 6px -1px rgba(16, 24, 40, 0.08);
        --sb-shadow-lg: 0 10px 15px -3px rgba(16, 24, 40, 0.08);
        --sb-radial-glow: none;
        --sb-heading-gradient: linear-gradient(135deg, #0f172a 40%, #334155 100%);
        --sb-brand-gradient: linear-gradient(135deg, #0f172a 30%, #475569 100%);
        --sb-metric-gradient: linear-gradient(135deg, #0f172a 40%, #4338ca 100%);
        """

    return f"""
    <style>
    /* Google Fonts: Inter Display & JetBrains Mono */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root,
    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"] {{
        color-scheme: {color_scheme} !important;
        --background-color: var(--sb-bg) !important;
        --secondary-background-color: var(--sb-surface-muted) !important;
        --text-color: var(--sb-text-main) !important;
        --primary-color: var(--sb-primary) !important;
        {vars_css}
    }}

    /* Global Dark-Tech Midnight Navy Canvas */
    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    section.main,
    .main,
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stBottomBlockContainer"] {{
        background-color: {"#080b14" if is_dark else "var(--sb-bg)"} !important;
        background-image: {"radial-gradient(ellipse 80% 50% at 50% -15%, rgba(99, 102, 241, 0.12), transparent 70%)" if is_dark else "none"} !important;
        color: var(--sb-text-main) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        letter-spacing: -0.011em;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] svg {{
        color: var(--sb-text-muted) !important;
        fill: var(--sb-text-muted) !important;
    }}

    /* Sidebar Overrides */
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] {{
        background-color: var(--sb-surface) !important;
        color: var(--sb-text-main) !important;
        border-right: 1px solid var(--sb-border) !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {{
        color: var(--sb-text-main) !important;
    }}

    /* Main Container Layout */
    .block-container,
    [data-testid="stMainBlockContainer"] {{
        padding-top: 1.25rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1240px !important;
        background-color: transparent !important;
    }}

    /* Anti-Stale interaction rules: CRITICAL FOR CAMERA LOOPS */
    div[data-stale="true"],
    .stApp [data-stale="true"],
    [data-testid="stAppViewContainer"] [data-stale="true"],
    [data-testid="stElementContainer"][data-stale="true"],
    [data-testid="stMainBlockContainer"][data-stale="true"] {{
        opacity: 1 !important;
        filter: none !important;
        pointer-events: auto !important;
        transition: none !important;
    }}
    .stButton > button {{
        pointer-events: auto !important;
    }}

    /* Streamlit Global Typography Overrides */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--sb-text-main) !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
    }}
    div[data-testid="stMarkdownContainer"],
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] div,
    div[data-testid="stText"],
    p, span, label,
    .stWidgetLabel label,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {{
        color: var(--sb-text-main) !important;
    }}
    div[data-testid="stCaptionContainer"] p,
    div[data-testid="stCaptionContainer"] span {{
        color: var(--sb-text-muted) !important;
    }}
    hr {{
        border: none !important;
        border-top: 1px solid var(--sb-border) !important;
        margin: 2rem 0 !important;
    }}
    code {{
        background-color: var(--sb-surface-muted) !important;
        color: var(--sb-primary-hover) !important;
        border: 1px solid var(--sb-border) !important;
        padding: 0.15rem 0.4rem !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85em !important;
    }}

    /* Refined Modern Buttons with Rounded Corners & Glow */
    .stButton > button,
    div[data-testid="stButton"] > button,
    div[class*="st-key-"] > button {{
        border-radius: 8px !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        min-height: 40px !important;
        padding: 0.5rem 1.15rem !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        letter-spacing: -0.01em !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        user-select: none !important;
        text-decoration: none !important;
        outline: none !important;
        border: 1px solid var(--sb-border) !important;
        background-color: var(--sb-surface-muted) !important;
        color: var(--sb-text-main) !important;
        backdrop-filter: blur(8px) !important;
    }}

    .stButton > button:hover,
    div[data-testid="stButton"] > button:hover {{
        border-color: var(--sb-primary) !important;
        background-color: var(--sb-surface-highlight) !important;
        color: var(--sb-text-main) !important;
        box-shadow: 0 0 14px rgba(99, 102, 241, 0.25) !important;
        transform: translateY(-1px) !important;
    }}

    .stButton > button:focus-visible,
    div[data-testid="stButton"] > button:focus-visible {{
        outline: 2px solid var(--sb-primary) !important;
        outline-offset: 2px !important;
    }}

    .stButton > button:active,
    div[data-testid="stButton"] > button:active {{
        transform: translateY(0px) !important;
    }}

    /* Primary Electric Indigo Button */
    button[kind="primary"],
    button[data-testid="baseButton-primary"],
    div.stButton > button[kind="primary"],
    div[data-testid="stButton"] > button[kind="primary"] {{
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    }}

    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stButton"] > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.35) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45) !important;
        transform: translateY(-1px) !important;
    }}

    /* Disabled State */
    .stButton > button:disabled,
    div[data-testid="stButton"] > button:disabled,
    button[disabled] {{
        opacity: 0.38 !important;
        cursor: not-allowed !important;
        pointer-events: none !important;
        box-shadow: none !important;
        transform: none !important;
    }}

    /* Rounded Pill Status Chips */
    .sb-status-chip {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--sb-chip-bg);
        border: 1px solid var(--sb-border);
        border-radius: 999px;
        padding: 0.32rem 0.85rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--sb-text-main);
    }}
    .sb-status-dot {{
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
    }}
    .sb-dot-ready, .sb-dot-pass {{
        background-color: #10b981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.7);
    }}
    .sb-dot-active, .sb-dot-processing {{
        background-color: #6366f1;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.7);
    }}
    .sb-dot-cyan {{
        background-color: #06b6d4;
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.7);
    }}
    .sb-dot-warning {{
        background-color: #f59e0b;
        box-shadow: 0 0 8px rgba(245, 158, 11, 0.6);
    }}
    .sb-dot-error, .sb-dot-fail {{
        background-color: #ef4444;
        box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
    }}
    .sb-dot-neutral {{
        background-color: #64748b;
    }}

    /* Navigation Header */
    .sb-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.85rem 0;
        border-bottom: 1px solid var(--sb-border);
        margin-bottom: 1.25rem;
    }}
    .sb-brand {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}
    .sb-brand-logo {{
        width: 34px;
        height: 34px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(6, 182, 212, 0.15) 100%);
        border: 1px solid var(--sb-border-strong);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.95rem;
        color: #ffffff;
        box-shadow: 0 0 14px rgba(99, 102, 241, 0.3);
    }}
    .sb-brand-name {{
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--sb-text-main);
        letter-spacing: -0.025em;
        background: var(--sb-brand-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .sb-brand-badge {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        background: var(--sb-chip-bg);
        color: var(--sb-primary-hover);
        border: 1px solid var(--sb-border);
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
    }}
    .sb-nav-tagline {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: var(--sb-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    /* Hero Section */
    .sb-hero-wrapper {{
        position: relative;
        padding: 3rem 0 2rem 0;
        background: var(--sb-radial-glow);
    }}
    .sb-hero-tag {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid var(--sb-border-strong);
        border-radius: 999px;
        padding: 0.35rem 0.95rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--sb-primary-hover);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 1.25rem;
        box-shadow: 0 0 14px rgba(99, 102, 241, 0.15);
    }}
    .sb-hero-title {{
        font-size: clamp(2.3rem, 5.2vw, 4rem);
        font-weight: 700;
        line-height: 1.08;
        letter-spacing: -0.035em;
        color: var(--sb-text-main);
        margin: 0 0 1.25rem 0;
        background: var(--sb-heading-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .sb-hero-sub {{
        font-size: 1.15rem;
        line-height: 1.6;
        color: var(--sb-text-muted);
        max-width: 580px;
        margin: 0 0 2rem 0;
    }}
    .sb-hero-notice {{
        font-size: 0.82rem;
        line-height: 1.5;
        color: var(--sb-text-subtle);
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid var(--sb-border);
    }}

    /* Hero Visual Mockup Window */
    .sb-preview-window {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 12px 36px -4px rgba(0, 0, 0, 0.7), 0 0 24px rgba(99, 102, 241, 0.15);
        backdrop-filter: blur(12px);
    }}
    .sb-preview-header {{
        background: var(--sb-surface-muted);
        border-bottom: 1px solid var(--sb-border);
        padding: 0.75rem 1.15rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--sb-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    .sb-preview-dots {{
        display: flex;
        gap: 6px;
    }}
    .sb-dot {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.22);
    }}
    .sb-preview-body {{
        padding: 1.5rem;
    }}
    .sb-preview-screen {{
        background: rgba(8, 11, 20, 0.85);
        border: 1px solid var(--sb-border-subtle);
        border-radius: 10px;
        padding: 2rem 1.5rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }}
    .sb-preview-overlay {{
        position: absolute;
        top: 10px;
        left: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #06b6d4;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    .sb-preview-pill {{
        margin-top: 1.25rem;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 999px;
        padding: 0.35rem 0.95rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        color: #10b981;
        letter-spacing: 0.08em;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.15);
    }}
    .sb-preview-footer {{
        margin-top: 0.75rem;
        background: rgba(8, 11, 20, 0.9);
        border: 1px solid var(--sb-border-subtle);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
        color: #ffffff;
        letter-spacing: 0.06em;
    }}

    /* Section Headers */
    .sb-section-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: #818cf8;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.5rem;
    }}
    .sb-section-heading {{
        font-size: clamp(1.6rem, 3.5vw, 2.5rem);
        font-weight: 700;
        color: var(--sb-text-main);
        letter-spacing: -0.03em;
        margin: 0 0 0.65rem 0;
    }}
    .sb-section-desc {{
        font-size: 0.98rem;
        color: var(--sb-text-muted);
        line-height: 1.6;
        max-width: 680px;
        margin-bottom: 2rem;
    }}

    /* Bento Feature Grid with Glassmorphic Midnight Navy Cards */
    .sb-bento-card {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 14px;
        padding: 1.75rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        backdrop-filter: blur(12px);
    }}
    .sb-bento-card:hover {{
        border-color: var(--sb-border-strong);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(99, 102, 241, 0.18);
        transform: translateY(-2px);
    }}
    .sb-bento-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.25rem;
    }}
    .sb-bento-num {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: #818cf8;
        letter-spacing: 0.08em;
    }}
    .sb-bento-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--sb-text-main);
        margin: 0 0 0.65rem 0;
        letter-spacing: -0.02em;
    }}
    .sb-bento-text {{
        font-size: 0.88rem;
        color: var(--sb-text-muted);
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }}
    .sb-bento-visual {{
        background: var(--sb-surface-muted);
        border: 1px solid var(--sb-border-subtle);
        border-radius: 10px;
        padding: 1.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 110px;
    }}

    /* Step Cards */
    .sb-step-card {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 14px;
        padding: 1.65rem;
        height: 100%;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        backdrop-filter: blur(12px);
    }}
    .sb-step-card:hover {{
        border-color: var(--sb-border-strong);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.5), 0 0 16px rgba(99, 102, 241, 0.15);
        transform: translateY(-2px);
    }}
    .sb-step-num {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: #818cf8;
        letter-spacing: 0.08em;
        margin-bottom: 0.75rem;
    }}
    .sb-step-title {{
        font-size: 1.12rem;
        font-weight: 700;
        color: var(--sb-text-main);
        margin: 0 0 0.5rem 0;
    }}
    .sb-step-text {{
        font-size: 0.86rem;
        color: var(--sb-text-muted);
        line-height: 1.6;
    }}

    /* 4-Column Large Monospace Metrics */
    .sb-metric-card {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: left;
        backdrop-filter: blur(12px);
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .sb-metric-card:hover {{
        border-color: var(--sb-border-strong);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5), 0 0 16px rgba(99, 102, 241, 0.15);
        transform: translateY(-2px);
    }}
    .sb-metric-val {{
        font-family: 'JetBrains Mono', monospace;
        font-size: clamp(2.2rem, 4vw, 3.4rem);
        font-weight: 700;
        color: var(--sb-text-main);
        line-height: 1;
        letter-spacing: -0.04em;
        margin-bottom: 0.5rem;
        background: var(--sb-metric-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .sb-metric-val-unit {{
        font-size: 1.1rem;
        font-weight: 600;
        color: #06b6d4;
        margin-left: 0.3rem;
        -webkit-text-fill-color: #06b6d4;
    }}
    .sb-metric-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--sb-text-main);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }}
    .sb-metric-desc {{
        font-size: 0.82rem;
        color: var(--sb-text-muted);
        line-height: 1.45;
    }}

    /* Technical Event Stream / Observability Dashboard */
    .sb-telemetry-panel {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(12px);
    }}
    .sb-telemetry-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--sb-border);
        margin-bottom: 1rem;
    }}
    .sb-telemetry-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--sb-text-main);
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }}
    .sb-event-table {{
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }}
    .sb-event-row {{
        display: grid;
        grid-template-columns: 85px 180px 1fr 110px;
        align-items: center;
        gap: 1rem;
        padding: 0.65rem 0.95rem;
        background: var(--sb-surface-muted);
        border: 1px solid var(--sb-border-subtle);
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        transition: border-color 0.15s ease;
    }}
    .sb-event-row:hover {{
        border-color: var(--sb-border-strong);
    }}
    .sb-event-time {{
        color: var(--sb-text-subtle);
    }}
    .sb-event-id {{
        color: #818cf8;
        font-weight: 600;
    }}
    .sb-event-msg {{
        color: var(--sb-text-muted);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    /* Live Recognition Workspace Panels */
    .sb-panel-box {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 14px;
        padding: 1.35rem;
        margin-bottom: 1.25rem;
        backdrop-filter: blur(12px);
    }}
    .sb-panel-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--sb-border);
        margin-bottom: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--sb-text-main);
    }}

    /* Sentence Output Box */
    .sb-sentence-output {{
        background: var(--sb-surface-muted);
        border: 1px solid var(--sb-border);
        border-radius: 10px;
        padding: 1.25rem 1.4rem;
        font-family: 'JetBrains Mono', monospace;
        color: var(--sb-text-main);
        line-height: 1.5;
        letter-spacing: 0.04em;
        word-break: break-word;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.08);
    }}

    /* Translation Container */
    .sb-translation-container {{
        background: var(--sb-surface-muted);
        border: 1px solid var(--sb-border-strong);
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin: 1rem 0;
        position: relative;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.12);
    }}
    .sb-translation-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--sb-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    .sb-translation-badge {{
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid var(--sb-border-strong);
        border-radius: 999px;
        padding: 0.25rem 0.65rem;
        font-weight: 600;
        color: #818cf8;
    }}
    .sb-translation-output {{
        font-size: 1.45rem;
        font-weight: 600;
        color: var(--sb-text-main);
        line-height: 1.5;
        letter-spacing: 0.02em;
    }}

    /* Badges & Telemetry Readouts */
    .sb-badge-detected {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 0.4rem 0.95rem;
        border-radius: 999px;
        border: 1px solid var(--sb-border);
        background: var(--sb-chip-bg);
        color: var(--sb-text-main);
    }}
    .sb-badge-success {{
        border-color: rgba(16, 185, 129, 0.4);
        color: #10b981;
        background: rgba(16, 185, 129, 0.12);
    }}
    .sb-badge-neutral {{
        color: var(--sb-text-muted);
    }}
    .sb-badge-warning {{
        color: #f59e0b;
        border-color: rgba(245, 158, 11, 0.4);
        background: rgba(245, 158, 11, 0.12);
    }}

    /* Camera Offline Placeholder */
    .sb-cam-offline {{
        background: var(--sb-surface-muted);
        border: 1px dashed var(--sb-border);
        border-radius: 12px;
        padding: 3.5rem 1.5rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}

    /* Callout Card */
    .sb-callout {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        backdrop-filter: blur(12px);
    }}
    .sb-callout-title {{
        font-weight: 600;
        color: var(--sb-text-main);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .sb-callout-text {{
        font-size: 0.86rem;
        color: var(--sb-text-muted);
        line-height: 1.6;
    }}

    /* Alphabet Matrix Grid */
    .sb-matrix-cell {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 10px;
        padding: 0.75rem 0.5rem;
        text-align: center;
        margin-bottom: 0.65rem;
        transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
        backdrop-filter: blur(8px);
    }}
    .sb-matrix-cell:hover {{
        border-color: var(--sb-border-strong);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }}
    .sb-matrix-letter {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--sb-text-main);
        margin-bottom: 0.25rem;
    }}
    .sb-matrix-badge-active {{
        display: block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.64rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #10b981;
        background: rgba(16, 185, 129, 0.15);
        padding: 2px 4px;
        border-radius: 999px;
    }}
    .sb-matrix-badge-ready {{
        display: block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.64rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #818cf8;
        background: rgba(99, 102, 241, 0.15);
        padding: 2px 4px;
        border-radius: 999px;
    }}
    .sb-matrix-badge-needs {{
        display: block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.64rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748b;
        background: var(--sb-surface-muted);
        padding: 2px 4px;
        border-radius: 999px;
    }}

    /* Onboarding Card */
    .sb-onboarding-card {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(12px);
    }}
    .sb-onboarding-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--sb-border);
    }}
    .sb-onboarding-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.25rem;
    }}
    .sb-onboarding-step {{
        background: var(--sb-surface-muted);
        border: 1px solid var(--sb-border-subtle);
        border-radius: 10px;
        padding: 1.15rem;
    }}
    .sb-onboarding-step-num {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: #818cf8;
        margin-bottom: 0.35rem;
    }}
    .sb-onboarding-step-title {{
        font-weight: 600;
        font-size: 0.92rem;
        color: var(--sb-text-main);
        margin-bottom: 0.35rem;
    }}
    .sb-onboarding-step-desc {{
        font-size: 0.8rem;
        color: var(--sb-text-muted);
        line-height: 1.45;
    }}

    /* Demo Mode Banner */
    .sb-demo-banner {{
        background: var(--sb-surface-muted);
        border: 1px solid var(--sb-border-strong);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.12);
    }}
    .sb-demo-badge {{
        display: inline-flex;
        align-items: center;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid var(--sb-border-strong);
        color: #818cf8;
        border-radius: 999px;
        padding: 0.2rem 0.65rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
    }}

    /* History Chips */
    .sb-history-chip {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: var(--sb-surface-muted);
        border: 1px solid var(--sb-border);
        border-radius: 6px;
        padding: 0.35rem 0.65rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        margin: 0.2rem;
    }}
    .sb-history-sign {{
        font-weight: 700;
        color: #818cf8;
    }}
    .sb-history-meta {{
        font-size: 0.68rem;
        color: var(--sb-text-subtle);
    }}

    /* Practice Mode Card */
    .sb-practice-card {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        backdrop-filter: blur(12px);
    }}
    .sb-practice-target {{
        font-size: 2.8rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: #818cf8;
        line-height: 1;
    }}

    /* Custom Command Card in Studio */
    .sb-command-card {{
        background: var(--sb-surface);
        border: 1px solid var(--sb-border);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
        backdrop-filter: blur(12px);
    }}
    .sb-command-card:hover {{
        border-color: var(--sb-border-strong);
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.15);
    }}

    /* Pulse Flash on Added Sign */
    .sb-added-pulse {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        color: #10b981;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
    }}

    /* Footer */
    .sb-footer {{
        margin-top: 5rem;
        padding-top: 2.5rem;
        border-top: 1px solid var(--sb-border);
        color: var(--sb-text-subtle);
        font-size: 0.84rem;
    }}
    .sb-footer-brand {{
        font-weight: 700;
        color: var(--sb-text-main);
        font-size: 1.15rem;
        letter-spacing: -0.02em;
        margin-bottom: 0.4rem;
    }}
    .sb-footer-col-title {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        color: var(--sb-text-main);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.65rem;
    }}
    .sb-footer-text {{
        color: var(--sb-text-muted);
        line-height: 1.6;
        font-size: 0.82rem;
    }}

    /* Streamlit Tabs Styling */
    div[data-baseweb="tab-list"] {{
        gap: 8px !important;
        background-color: transparent !important;
        border-bottom: 1px solid var(--sb-border) !important;
        padding-bottom: 4px !important;
        margin-bottom: 1.5rem !important;
    }}
    button[data-baseweb="tab"] {{
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 8px 8px 0 0 !important;
        color: var(--sb-text-muted) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1.25rem !important;
        transition: all 0.2s ease !important;
    }}
    button[data-baseweb="tab"]:hover {{
        color: var(--sb-text-main) !important;
        background: var(--sb-surface-muted) !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: var(--sb-primary-hover) !important;
        background: var(--sb-surface) !important;
        border: 1px solid var(--sb-border) !important;
        border-bottom: 2px solid var(--sb-primary) !important;
        box-shadow: 0 -2px 10px rgba(99, 102, 241, 0.15) !important;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: var(--sb-primary) !important;
    }}
    div[data-baseweb="tab-border"] {{
        background-color: var(--sb-border) !important;
    }}

    /* Streamlit Input & TextArea Overrides */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    input.stTextInput,
    textarea.stTextArea {{
        background-color: var(--sb-surface-muted) !important;
        border: 1px solid var(--sb-border) !important;
        border-radius: 8px !important;
        color: var(--sb-text-main) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }}
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {{
        border-color: var(--sb-primary) !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.25) !important;
    }}
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {{
        color: var(--sb-text-main) !important;
    }}

    /* Slider Overrides */
    div[data-testid="stSlider"] {{
        padding: 0.5rem 0 !important;
    }}
    div[data-testid="stSlider"] div[role="slider"] {{
        background-color: var(--sb-primary) !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.5) !important;
    }}

    /* Expander Overrides */
    div[data-testid="stExpander"] {{
        background: var(--sb-surface) !important;
        border: 1px solid var(--sb-border) !important;
        border-radius: 10px !important;
        margin-bottom: 1rem !important;
        overflow: hidden !important;
        backdrop-filter: blur(8px) !important;
    }}
    div[data-testid="stExpander"] summary {{
        color: var(--sb-text-main) !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
    }}
    div[data-testid="stExpander"] summary:hover {{
        color: var(--sb-primary-hover) !important;
    }}
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
        padding: 1rem !important;
        border-top: 1px solid var(--sb-border-subtle) !important;
    }}

    /* Progress Bar Overrides */
    div[data-testid="stProgress"] > div > div > div > div {{
        background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%) !important;
        border-radius: 999px !important;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.5) !important;
    }}
    div[data-testid="stProgress"] > div > div > div {{
        background-color: var(--sb-surface-muted) !important;
        border-radius: 999px !important;
    }}

    /* Streamlit Widget Theme Overrides */
    div[data-testid="stToggle"] label p,
    div[data-testid="stCheckbox"] label p,
    div[data-testid="stRadio"] label p {{
        color: var(--sb-text-main) !important;
        font-size: 0.88rem !important;
    }}

    div[data-baseweb="select"] {{
        border-radius: 8px !important;
        background-color: var(--sb-surface-muted) !important;
        border: 1px solid var(--sb-border) !important;
    }}
    div[data-baseweb="select"] * {{
        color: var(--sb-text-main) !important;
        background-color: transparent !important;
        font-family: 'Inter', sans-serif !important;
    }}
    div[data-baseweb="popover"],
    div[data-baseweb="menu"] {{
        background-color: var(--sb-surface) !important;
        border: 1px solid var(--sb-border-strong) !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6) !important;
    }}
    div[data-baseweb="menu"] * {{
        color: var(--sb-text-main) !important;
        background-color: transparent !important;
    }}

    div[data-testid="stAlert"] {{
        background-color: var(--sb-surface-muted) !important;
        border: 1px solid var(--sb-border) !important;
        border-radius: 10px !important;
        color: var(--sb-text-main) !important;
    }}

    /* STRICT: Camera & Image Color Integrity (DO NOT INVERT OR FILTER) */
    [data-testid="stImage"] img,
    img {{
        filter: none !important;
        border-radius: 8px !important;
    }}
    </style>
    """
