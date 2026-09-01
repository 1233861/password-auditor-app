import streamlit as st
import math
import re


st.set_page_config(page_title="Password Strength Auditor", page_icon="🔐", layout="centered")

st.title("🔐 Password Security Auditor")
st.write("Enter a password below to analyze its strength, entropy, and vulnerabilities.")

# Password Input
password = st.text_input("Enter Password", type="password", help="Type your password here to test.")

if password:
    # Get audit metrics (agar auditor.py me direct function na ho to basic calculation)
    length = len(password)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    # Calculate Pool Size & Entropy
    pool_size = 0
    if has_lower: pool_size += 26
    if has_upper: pool_size += 26
    if has_digit: pool_size += 10
    if has_symbol: pool_size += 32
    
    entropy = round(length * math.log2(pool_size), 1) if pool_size > 0 else 0

    st.markdown("---")
    
    # Dashboard Metrics Columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Password Length", length)
    col2.metric("Character Pool", pool_size)
    col3.metric("Entropy", f"{entropy} bits")

    # Strength Indicator
    st.subheader("Strength Score")
    if entropy < 28:
        st.error("🔴 Very Weak")
    elif entropy < 36:
        st.warning("🟠 Weak")
    elif entropy < 60:
        st.info("🟡 Reasonable")
    elif entropy < 128:
        st.success("🟢 Strong")
    else:
        st.success("🟢 Very Strong (Very High Security)")

    # Checklist / Character Mix
    st.subheader("Character Checklist")
    c1, c2, c3, c4 = st.columns(4)
    c1.checkbox("Lowercase (a-z)", value=has_lower, disabled=True)
    c2.checkbox("Uppercase (A-Z)", value=has_upper, disabled=True)
    c3.checkbox("Numbers (0-9)", value=has_digit, disabled=True)
    c4.checkbox("Symbols (!@#$)", value=has_symbol, disabled=True)

    # Suggestions
    st.subheader("💡 Suggestions to Improve")
    suggestions = []
    if length < 12: suggestions.append("Use at least 12 characters.")
    if not has_upper: suggestions.append("Add uppercase letters (A-Z).")
    if not has_digit: suggestions.append("Add numbers (0-9).")
    if not has_symbol: suggestions.append("Add symbols (e.g. !@#$%).")
    
    if suggestions:
        for s in suggestions:
            st.write(f"- {s}")
    else:
        st.write("✨ Great job! Your password meets all basic security criteria.")