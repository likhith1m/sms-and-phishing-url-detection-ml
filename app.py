import streamlit as st
import random
import time
import pandas as pd
import numpy as np
import plotly.express as px
from sms_module import analyze_sms
from url_module import analyze_url

st.set_page_config(
    page_title="Rakshak AI - Cyber Command Center",
    page_icon="🛡️",
    layout="wide"
)

# SESSION STATE
if "security_score" not in st.session_state:
    st.session_state.security_score = 85

if "threat_history" not in st.session_state:
    st.session_state.threat_history = []

# DARK THEME
st.markdown("""
<style>
body {background-color:#0e1117;}
.big-title {font-size:40px;font-weight:bold;}
.high {background:#3b0d0d;padding:15px;border-left:5px solid red;border-radius:10px;}
.medium {background:#3b2d0d;padding:15px;border-left:5px solid orange;border-radius:10px;}
.low {background:#0d3b1f;padding:15px;border-left:5px solid green;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🛡️ RAKSHAK AI</div>', unsafe_allow_html=True)
st.subheader("Enterprise Multi-Vector Cyber Defense Platform")
st.divider()

learning_mode = st.toggle("🧠 AI Learning Mode")

tab1, tab2, tab3 = st.tabs(["📩 SMS", "🌐 URL", "🛰 Dashboard"])

# ================= SMS =================
with tab1:
    sms_input = st.text_area("Enter SMS")

    if st.button("Analyze SMS"):
        result = analyze_sms(sms_input)
        score = result["risk_score"]

        if learning_mode and score > 50:
            score += 5

        score = min(score, 100)
        st.progress(score)
        st.write(f"Risk Score: {score}/100")

        if score > 70:
            st.markdown('<div class="high">🚨 HIGH RISK SMS</div>', unsafe_allow_html=True)
            st.session_state.security_score -= 10
        elif score > 40:
            st.markdown('<div class="medium">⚠️ SUSPICIOUS SMS</div>', unsafe_allow_html=True)
            st.session_state.security_score -= 5
        else:
            st.markdown('<div class="low">✅ SAFE SMS</div>', unsafe_allow_html=True)

        st.session_state.threat_history.append(score)

# ================= URL =================
with tab2:
    url_input = st.text_input("Enter URL")

    if st.button("Analyze URL"):
        result = analyze_url(url_input)
        score = result["risk_score"]

        if learning_mode and score > 50:
            score += 5

        score = min(score, 100)
        st.progress(score)
        st.write(f"Risk Score: {score}/100")

        if score > 70:
            st.markdown('<div class="high">🚨 MALICIOUS URL</div>', unsafe_allow_html=True)
            st.session_state.security_score -= 10
        elif score > 40:
            st.markdown('<div class="medium">⚠️ SUSPICIOUS URL</div>', unsafe_allow_html=True)
            st.session_state.security_score -= 5
        else:
            st.markdown('<div class="low">✅ SAFE URL</div>', unsafe_allow_html=True)

        st.session_state.threat_history.append(score)

# ================= DASHBOARD =================
with tab3:

    st.subheader("🚨 Live Attack Feed")
    events = [
        "Phishing SMS detected (India)",
        "Malicious domain blocked (USA)",
        "Suspicious login attempt (Russia)",
        "Banking scam detected (Nigeria)"
    ]
    st.write(random.choice(events))

    st.divider()

    st.subheader("📊 Threat Trend Analytics")
    if st.session_state.threat_history:
        df = pd.DataFrame({"Threat Score": st.session_state.threat_history})
        fig = px.line(df, y="Threat Score", title="Threat Score Trend")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🌍 Global Threat Map (Simulated)")
    map_data = pd.DataFrame({
        "lat": [28.6, 55.7, 40.7, 35.6],
        "lon": [77.2, 37.6, -74.0, 139.6]
    })
    st.map(map_data)

    st.divider()

    st.subheader("🌡 Threat Heatmap")
    heatmap_data = np.random.randint(0, 100, (5, 5))
    heatmap_df = pd.DataFrame(heatmap_data)
    st.dataframe(heatmap_df.style.background_gradient(cmap="Reds"))

    st.divider()

    st.subheader("🛰 Radar Scanner")
    radar = st.empty()
    for i in range(3):
        radar.markdown("<h3 style='color:lime'>Scanning...</h3>", unsafe_allow_html=True)
        time.sleep(0.5)
    radar.markdown("<h3 style='color:red'>Threat Signals Detected!</h3>", unsafe_allow_html=True)

    st.divider()

    st.subheader("📈 Security Posture Score")
    score = max(st.session_state.security_score, 0)
    if score > 70:
        st.success(f"🟢 Secure ({score}/100)")
    elif score > 40:
        st.warning(f"🟡 Elevated Risk ({score}/100)")
    else:
        st.error(f"🔴 Critical Risk ({score}/100)")

    st.divider()

    st.subheader("🎭 Simulate Attack")
    if st.button("Launch Fake Attack"):
        fake_score = random.randint(60, 100)
        st.session_state.threat_history.append(fake_score)
        st.session_state.security_score -= 15
        st.error("🚨 Simulated Attack Injected!")
        time.sleep(1)
        st.rerun()