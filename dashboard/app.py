import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cardio AI Dashboard", page_icon="💓", layout="wide")
st.title("💓 Cardio AI — Wellness Pattern Dashboard")
st.caption("Academic prototype. Synthetic simulator data is labeled; this is not a medical diagnostic system.")
api = st.sidebar.text_input("Backend URL", "http://127.0.0.1:8000").rstrip("/")
refresh = st.sidebar.button("Refresh data")

try:
    response = requests.get(f"{api}/readings", params={"limit": 1000}, timeout=5)
    response.raise_for_status()
    records = response.json()
except (requests.RequestException, ValueError) as exc:
    st.error(f"Cannot reach the API at {api}. Start the backend, then refresh. Details: {exc}")
    st.stop()

df = pd.DataFrame(records)
if df.empty:
    st.info("No readings recorded yet. Start the simulator or connect a supported device.")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
latest = df.iloc[-1]
a, b, c, d = st.columns(4)
def metric(col, title, field, suffix=""):
    value = latest.get(field)
    col.metric(title, "—" if pd.isna(value) else f"{value:g}{suffix}")
metric(a, "Heart rate", "heart_rate", " bpm")
metric(b, "SpO₂", "spo2", "%")
metric(c, "HRV", "hrv", " ms")
metric(d, "Steps", "steps")

st.subheader("Measurement trends")
for field, label in [("heart_rate", "Heart rate (bpm)"), ("spo2", "SpO₂ (%)"), ("hrv", "HRV (ms)")]:
    if field in df and df[field].notna().any():
        st.markdown(f"**{label}**")
        st.line_chart(df.set_index("timestamp")[field])

st.subheader("Exploratory AI pattern status")
try:
    result = requests.get(f"{api}/anomaly", timeout=15)
    result.raise_for_status()
    result = result.json()
    status = result.get("status", "UNKNOWN")
    if status == "UNUSUAL_PATTERN":
        st.warning("The model marked the latest sample as unusual relative to this dataset. This is not a diagnosis.")
    elif status == "NO_UNUSUAL_PATTERN":
        st.success("The model did not mark the latest sample as unusual relative to this dataset.")
    else:
        st.info(result.get("message", "More valid observations are needed."))
    st.json(result)
except (requests.RequestException, ValueError) as exc:
    st.warning(f"AI endpoint unavailable: {exc}")

st.subheader("Recent readings")
display = df.sort_values("timestamp", ascending=False).copy()
display["timestamp"] = display["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S UTC")
st.dataframe(display, use_container_width=True, hide_index=True)
st.caption("Data source is shown in the device column. Simulator values are artificial test data, not real wearable measurements.")
