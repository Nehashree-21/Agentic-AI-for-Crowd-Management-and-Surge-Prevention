import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Agentic AI Crowd Management",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Agentic AI-Based Crowd Management")
st.subheader("Surge Prevention and Threat Detection Dashboard")

# Check backend connection
try:
    response = requests.get(f"{API_URL}/health", timeout=3)
    backend_status = response.json().get("status", "unknown")
except requests.RequestException:
    backend_status = "offline"

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Crowd Count", "0")

with col2:
    st.metric("Density", "Normal")

with col3:
    st.metric("Surge Risk", "LOW")

with col4:
    st.metric("Threat Status", "No Threat")

st.divider()

st.subheader("Live Video Feed")
st.info("Video processing will be integrated in the next milestones.")

st.subheader("Agent Decision")
st.success("System initialized. Monitoring environment...")

st.divider()

st.subheader("Backend Connection")

if backend_status == "healthy":
    st.success("FastAPI backend is connected and healthy")
else:
    st.error("FastAPI backend is offline")
    st.caption("Make sure uvicorn is running on port 8000.")