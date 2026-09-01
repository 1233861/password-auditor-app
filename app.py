import streamlit as st
import math
import re

# 1. Page Config
st.set_page_config(
    page_title="Password Security Auditor", 
    page_icon="🛡️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. VIP Styling & Ultimate Clean Layout CSS
vip_style = """
    <style>
    /* Hide Default Streamlit Headers, Footers, & Floating Badges */
    #MainMenu {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stElementToolbar"] {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    div[class*="stActionButton"] {display: none !important;}
    button[title*="Manage app"] {display: none !important;}
    .stAppIconButton {display: none !important;}
    .stApp > header {display: none !important;}

    /* Global Dark Modern Theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    /* Container Spacing */
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 720px;
    }

    /* Hero Header Styling */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-align: center;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        text-align: center;
        margin-bottom: 1.8rem;
    }

    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        text-align: center;
    }

    div[data-testid="stMetricLabel"] > label {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] > div {
        color: #38bdf8 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    /* Input Field Customization */
    div[data-baseweb="input"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 3px solid #38bdf8;
        padding-left: 8px;
    }

    /* Custom Strength Cards */
    .strength-card {
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .v-weak { background: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.3); }
    .weak { background: rgba(249, 115, 22, 0.15); color: #fdba74; border: 1px solid rgba(249, 115, 22, 0.3); }
    .medium { background: rgba(234, 179, 8, 0.15); color: #fde047; border: 1px solid rgba(234, 179, 8, 0.3); }
    .strong { background: rgba(34, 197, 94, 0.15); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.3); }
    .v-strong { background: rgba(16, 185, 129, 0.2); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.4); box-shadow: 0 0 12px rgba(16, 185, 129, 0.2); }

    /* Suggestion Box */
    .suggestion-item {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 6px;
        font-size: 0.9rem;
        color: #cbd5e1;
    }

    /* Professional Footer */
    .custom-footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    .custom-footer span {
        color: #38bdf8;
        font-weight: 600;
    }
    </style>
"""
st.markdown(vip_style, unsafe_allow_html=True)

# 3. Header UI
st.markdown('<div class="hero-title">🛡️ Password Auditor</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Real-time entropy analysis, strength scoring & security checklist</div>', unsafe_allow_html=True)

# 4. Input UI
password = st.text_input("Enter Password", type="password", placeholder="Type password here...", help="Your password is evaluated locally and never saved.")

if password:
    # Calculations
    length = len(password)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    pool_size = 0
    if has_lower: pool_size += 26
    if has_upper: pool_size += 26
    if has_digit: pool_size += 10
    if has_symbol: pool_size += 32
    
    entropy = round(length * math.log2(pool_size), 1) if pool_size > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics Grid
    col1, col2, col3 = st.columns(3)
    col1.metric("Length", f"{length} chars")
    col2.metric("Pool Size", pool_size)
    col3.metric("Entropy", f"{entropy} bits")

    # Strength Score Card
    st.markdown('<div class="section-header">Strength Score</div>', unsafe_allow_html=True)
    if entropy < 28:
        st.markdown('<div class="strength-card v-weak">🚨 Very Weak (High Risk)</div>', unsafe_allow_html=True)
    elif entropy < 36:
        st.markdown('<div class="strength-card weak">⚠️ Weak Password</div>', unsafe_allow_html=True)
    elif entropy < 60:
        st.markdown('<div class="strength-card medium">⚡ Reasonable Strength</div>', unsafe_allow_html=True)
    elif entropy < 128:
        st.markdown('<div class="strength-card strong">🛡️ Strong & Secure</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="strength-card v-strong">💎 VIP Level Security (Extremely Strong)</div>', unsafe_allow_html=True)

    # Checklist
    st.markdown('<div class="section-header">Character Checklist</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.checkbox("a-z", value=has_lower, disabled=True)
    c2.checkbox("A-Z", value=has_upper, disabled=True)
    c3.checkbox("0-9", value=has_digit, disabled=True)
    c4.checkbox("!@#$", value=has_symbol, disabled=True)

    # Suggestions
    st.markdown('<div class="section-header">💡 Security Recommendations</div>', unsafe_allow_html=True)
    suggestions = []
    if length < 12: suggestions.append("Increase length to at least 12 characters.")
    if not has_upper: suggestions.append("Include uppercase letters (A-Z).")
    if not has_digit: suggestions.append("Include numbers (0-9).")
    if not has_symbol: suggestions.append("Include special symbols (!@#$%).")
    
    if suggestions:
        for s in suggestions:
            st.markdown(f'<div class="suggestion-item">👉 {s}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="suggestion-item" style="color: #4ade80;">✨ Excellent! Your password follows all cybersecurity best practices.</div>', unsafe_allow_html=True)

# 5. Professional Footer Text
st.markdown('<div class="custom-footer">Designed & Developed by <span>Uzair Khoso</span> | Security Tool</div>', unsafe_allow_html=True)
