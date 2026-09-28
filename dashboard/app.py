import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cardio AI - Fire-Boltt", layout="wide")
st.title("⌚ Cardio AI — Fire-Boltt Dashboard")
st.caption("Academic anomaly-detection prototype; not a medical diagnostic system.")

API = st.sidebar.text_input(
    "Backend URL",
    "http://127.0.0.1:8000"
)

try:
    data = requests.get(f"{API}/readings", timeout=5).json()
    df = pd.DataFrame(data)

    if df.empty:
        st.info("No readings yet. Run the simulator or connect the Android app.")
    else:
        latest = df.iloc[0]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Heart Rate", f"{latest.get('heart_rate', '—')} BPM")
        c2.metric("SpO₂", f"{latest.get('spo2', '—')}%")
        c3.metric("HRV", f"{latest.get('hrv', '—')} ms")
        c4.metric("Steps", f"{latest.get('steps', '—')}")

        if "timestamp" in df and "heart_rate" in df:
            chart = df.copy()
            chart["timestamp"] = pd.to_datetime(
    chart["timestamp"],
    format="mixed",
    errors="coerce"
)
            chart = chart.sort_values("timestamp")
            st.subheader("Heart-rate trend")
            st.line_chart(chart.set_index("timestamp")["heart_rate"])

        try:
            result = requests.get(f"{API}/anomaly", timeout=5).json()
            st.subheader("AI status")
            st.write(result)
        except Exception as e:
            st.warning(f"AI endpoint unavailable: {e}")

        st.subheader("Recent readings")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Cannot connect to backend: {e}")
