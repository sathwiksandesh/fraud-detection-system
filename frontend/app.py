import streamlit as st
import random
import pandas as pd
import numpy as np
import requests

# =====================================================
# PAGE CONFIG (MUST BE FIRST)
# =====================================================
st.set_page_config(page_title="Fraud Detection", page_icon="🛡️")

# =====================================================
# GLASSMORPHISM STYLE
# =====================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.block-container {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 2rem;
}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.06);
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE INIT
# =====================================================
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None

if "require_otp" not in st.session_state:
    st.session_state.require_otp = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# =====================================================
# HEADER
# =====================================================
st.title("🛡️ Real-Time Fraud Detection Demo")
st.divider()
st.subheader("📈 Fraud Monitoring Dashboard")
st.caption("AI-powered transaction risk analysis")

col1, col2, col3 = st.columns(3)
col1.metric("Transactions Checked", 128)
col2.metric("Frauds Prevented", 7)
col3.metric("Detection Accuracy", "98.4%")

# =====================================================
# CHART
# =====================================================
#st.subheader("📉 Risk Trend (Demo)")
#chart_data = pd.DataFrame({"Risk Score": np.random.rand(20)})
#st.line_chart(chart_data)

# =====================================================
# INPUTS
# =====================================================
st.subheader("🧾 Transaction Details")

amount = st.number_input("💰 Transaction Amount", min_value=0.0)
time_gap = st.number_input("⏱️ Time Since Last Transaction", min_value=0.0)
device_score = st.slider("📱 Device Trust Score", 0.0, 1.0, 0.5)
location_risk = st.slider("🌍 Location Risk", 0.0, 1.0, 0.5)

# =====================================================
# CHECK BUTTON
# =====================================================
if st.button("🔍 Check Transaction"):

    # reset OTP each new transaction
    st.session_state.otp_sent = False
    st.session_state.generated_otp = None

    with st.spinner("Analyzing transaction..."):
        try:
            response = requests.post(
                "http://localhost:8000/check_transaction",
                json={
                    "amount": amount,
                    "time_gap": time_gap,
                    "device_score": device_score,
                    "location_risk": location_risk
                },
                timeout=10
            )

            result = response.json()
            st.session_state.last_result = result

            # =================================================
            # ⭐ YOUR CUSTOM OTP RULE
            # =================================================
            if device_score < 0.4 and location_risk > 0.6:
                st.session_state.require_otp = True
            else:
                st.session_state.require_otp = False

        except Exception as e:
            st.error(f"❌ Error connecting to backend: {e}")

# =====================================================
# RESULT DISPLAY (ALWAYS RUNS)
# =====================================================
if st.session_state.last_result is not None:

    result = st.session_state.last_result

    st.subheader("📊 Risk Analysis")
    st.metric("Fraud Probability", f"{result['fraud_probability']:.4f}")

    # -------------------------------------------------
    # CASE 1 — DIRECT ALLOW
    # -------------------------------------------------
    if result["action"] == "ALLOW" and not st.session_state.require_otp:
        st.success("✅ Transaction Allowed")

    # -------------------------------------------------
    # CASE 2 — OTP REQUIRED
    # -------------------------------------------------
    elif result["action"] == "STEP_UP_AUTH" or st.session_state.require_otp:

        st.warning("⚠️ Step-up Authentication Required")

        # Generate OTP once
        if not st.session_state.otp_sent:
            st.session_state.generated_otp = str(random.randint(100000, 999999))
            st.session_state.otp_sent = True

        st.info(f"🔐 OTP sent to user (demo): {st.session_state.generated_otp}")

        user_otp = st.text_input("Enter OTP", key="otp_input")

        if st.button("Verify OTP"):

            if user_otp == st.session_state.generated_otp:
                st.success("✅ OTP Verified — Transaction Allowed")
                st.session_state.otp_sent = False
                st.session_state.require_otp = False
            else:
                st.error("❌ Invalid OTP")

    # -------------------------------------------------
    # CASE 3 — BLOCK
    # -------------------------------------------------
    else:
        st.error("🚫 Transaction Blocked")