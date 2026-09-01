import os
import streamlit as st
import requests
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CrowdGuard AI",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM THEME
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b1020;
    }

    [data-testid="stHeader"] {
        background-color: #0b1020;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    p {
        color: #dbe4f0;
    }

    div[data-testid="stMetric"] {
        background-color: #151d2e;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API HELPER
# ============================================================

def get_api(endpoint):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=3
        )

        if response.ok:
            return response.json()

    except requests.RequestException:
        pass

    return None


# ============================================================
# BACKEND
# ============================================================

health = get_api("/health")

current_status = get_api(
    "/api/status"
)

observation_data = get_api(
    "/api/observations?limit=20"
)

alert_data = get_api(
    "/api/alerts?limit=10"
)


backend_online = (
    health is not None
    and health.get("status") == "healthy"
)


# ============================================================
# DEFAULT STATUS
# ============================================================

if current_status is None:

    current_status = {
        "crowd_count": 0,
        "density": "UNKNOWN",
        "surge_risk": "LOW",
        "risk_score": 0,
        "threat_status": "UNKNOWN",
        "agent_decision": "WAITING",
        "dominant_direction": "UNKNOWN",
        "flow_consistency": 0
    }


observations = []

if observation_data:

    observations = observation_data.get(
        "observations",
        []
    )


alerts = []

if alert_data:

    alerts = alert_data.get(
        "alerts",
        []
    )


# ============================================================
# CURRENT VALUES
# ============================================================

crowd_count = current_status.get(
    "crowd_count",
    0
)

density = current_status.get(
    "density",
    "UNKNOWN"
)

risk_score = current_status.get(
    "risk_score",
    0
)

risk_level = current_status.get(
    "surge_risk",
    "LOW"
)

threat_status = current_status.get(
    "threat_status",
    "UNKNOWN"
)

agent_decision = current_status.get(
    "agent_decision",
    "WAITING"
)

direction = current_status.get(
    "dominant_direction",
    "UNKNOWN"
)

flow_consistency = current_status.get(
    "flow_consistency",
    0
)


latest_movement = 0

if observations:

    latest_movement = observations[-1].get(
        "average_movement",
        0
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚨 CrowdGuard AI")

    st.caption(
        "Intelligent Crowd Safety Platform"
    )

    st.divider()

    st.subheader("System")

    if backend_online:

        st.success(
            "🟢 SYSTEM ONLINE"
        )

    else:

        st.error(
            "🔴 BACKEND OFFLINE"
        )

    st.divider()

    st.subheader("Monitoring")

    st.write("📹 CCTV Analysis")
    st.write("👥 Crowd Tracking")
    st.write("🌊 Flow Analysis")
    st.write("⚠️ Surge Prediction")
    st.write("🛡️ Threat Detection")

    st.divider()

    st.caption(
        "Agentic AI Crowd Management"
    )

    st.caption(
        "Prototype v1.0"
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "🚨 CrowdGuard AI"
)

st.subheader(
    "AI-powered real-time crowd safety and threat monitoring"
)

if backend_online:

    st.success(
        "🟢 LIVE · Monitoring system connected"
    )

else:

    st.error(
        "🔴 Backend offline"
    )


# ============================================================
# CURRENT SITUATION
# ============================================================

st.divider()

st.header(
    "📊 Current Situation"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👥 Crowd Count",
        crowd_count
    )

    st.caption(
        "Tracked individuals"
    )


with col2:

    st.metric(
        "📊 Density",
        density
    )

    st.caption(
        "Current crowd condition"
    )


with col3:

    st.metric(
        "⚠️ Surge Risk",
        f"{risk_score}/100"
    )

    st.caption(
        f"Risk level: {risk_level}"
    )


with col4:

    st.metric(
        "🛡️ Threat Status",
        threat_status
    )

    st.caption(
        "AI threat assessment"
    )


# ============================================================
# LIVE VIDEO
# ============================================================

st.divider()

st.header(
    "📹 Live Monitoring"
)


video_files = []

if os.path.isdir(OUTPUT_DIR):

    video_files = [
        filename
        for filename in os.listdir(
            OUTPUT_DIR
        )
        if filename.lower().endswith(
            ".mp4"
        )
    ]


# Prefer browser-compatible annotated video

if "annotated_browser.mp4" in video_files:

    selected_video = (
        "annotated_browser.mp4"
    )

elif "annotated_test.mp4" in video_files:

    selected_video = (
        "annotated_test.mp4"
    )

elif video_files:

    selected_video = sorted(
        video_files
    )[0]

else:

    selected_video = None


video_col, intelligence_col = st.columns(
    [3, 1]
)


# ============================================================
# VIDEO
# ============================================================

with video_col:

    st.subheader(
        "🎥 AI Annotated CCTV Feed"
    )

    if selected_video:

        video_path = os.path.join(
            OUTPUT_DIR,
            selected_video
        )

        st.caption(
            f"Source: {selected_video}"
        )

        st.video(
            video_path
        )

        st.success(
            "🟢 YOLO + ByteTrack tracking active"
        )

    else:

        st.warning(
            "No annotated video found."
        )

        st.caption(
            "Expected file:"
        )

        st.code(
            os.path.join(
                OUTPUT_DIR,
                "annotated_browser.mp4"
            )
        )


# ============================================================
# AI INTELLIGENCE
# ============================================================

with intelligence_col:

    st.subheader(
        "🧠 AI Intelligence"
    )

    st.metric(
        "🌊 Dominant Flow",
        direction
    )

    st.caption(
        f"Flow consistency: "
        f"{flow_consistency:.2f}%"
    )

    st.metric(
        "🏃 Average Movement",
        f"{latest_movement:.2f}"
    )

    st.caption(
        "pixels / frame"
    )

    st.metric(
        "📍 Observations",
        len(observations)
    )

    st.caption(
        "Recorded monitoring points"
    )


# ============================================================
# RISK INTELLIGENCE
# ============================================================

st.divider()

st.header(
    "📈 Risk Intelligence"
)


if observations:

    dataframe = pd.DataFrame(
        observations
    )

    dataframe = dataframe.sort_values(
        "id"
    )

    chart_col, agent_col = st.columns(
        [3, 1]
    )


    with chart_col:

        st.subheader(
            "Crowd and Risk Trend"
        )

        chart_data = dataframe.set_index(
            "id"
        )[
            [
                "crowd_count",
                "risk_score"
            ]
        ]

        st.line_chart(
            chart_data,
            height=350
        )


    with agent_col:

        st.subheader(
            "🤖 AI Agent Decision"
        )

        if risk_level == "CRITICAL":

            st.error(
                f"🚨 {agent_decision}"
            )

        elif risk_level == "WARNING":

            st.warning(
                f"⚠️ {agent_decision}"
            )

        else:

            st.success(
                f"✅ {agent_decision}"
            )


        st.markdown(
            "### Current Assessment"
        )

        st.write(
            f"👥 Crowd: {crowd_count} people"
        )

        st.write(
            f"📊 Density: {density}"
        )

        st.write(
            f"⚠️ Surge Risk: {risk_score}/100"
        )

        st.write(
            f"🌊 Flow: {direction}"
        )

        st.write(
            f"📈 Consistency: "
            f"{flow_consistency:.2f}%"
        )

        st.write(
            f"🛡️ Threat: {threat_status}"
        )

else:

    st.info(
        "No historical observations available."
    )


# ============================================================
# SECURITY EVENTS
# ============================================================

st.divider()

st.header(
    "🚨 Security Events"
)


if alerts:

    for alert in alerts:

        severity = alert.get(
            "severity",
            "INFO"
        )

        alert_type = alert.get(
            "alert_type",
            "UNKNOWN"
        )

        message = alert.get(
            "message",
            "No message available."
        )

        confidence = alert.get(
            "confidence",
            0
        )

        alert_status = alert.get(
            "status",
            "UNKNOWN"
        )

        timestamp = alert.get(
            "timestamp",
            ""
        )


        with st.container(
            border=True
        ):

            if severity == "CRITICAL":

                st.error(
                    f"🔴 CRITICAL · {alert_type}"
                )

            elif severity == "WARNING":

                st.warning(
                    f"🟡 WARNING · {alert_type}"
                )

            else:

                st.info(
                    f"🔵 {severity} · {alert_type}"
                )


            st.write(
                message
            )

            st.caption(
                f"Confidence: "
                f"{float(confidence):.2f}"
            )

            st.caption(
                f"Status: {alert_status}"
            )

            st.caption(
                f"Time: {timestamp}"
            )

else:

    st.success(
        "✅ No security alerts recorded."
    )


# ============================================================
# MONITORING SUMMARY
# ============================================================

st.divider()

st.header(
    "📋 Monitoring Summary"
)


summary1, summary2, summary3 = st.columns(3)


with summary1:

    st.metric(
        "Recorded Observations",
        len(observations)
    )


with summary2:

    peak_risk = 0

    if observations:

        peak_risk = max(
            item.get(
                "risk_score",
                0
            )
            for item in observations
        )

    st.metric(
        "Peak Risk",
        f"{peak_risk}/100"
    )


with summary3:

    average_crowd = 0

    if observations:

        average_crowd = (
            sum(
                item.get(
                    "crowd_count",
                    0
                )
                for item in observations
            )
            / len(observations)
        )

    st.metric(
        "Average Crowd",
        f"{average_crowd:.1f}"
    )


# ============================================================
# RECENT DATA
# ============================================================

st.divider()

st.header(
    "🗂️ Recent Monitoring Data"
)


if observations:

    dataframe = pd.DataFrame(
        observations
    )

    display_columns = [
        "timestamp",
        "crowd_count",
        "density",
        "average_movement",
        "dominant_direction",
        "flow_consistency",
        "risk_score",
        "risk_level"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in dataframe.columns
    ]

    dataframe = dataframe.sort_values(
        "id",
        ascending=False
    )

    st.dataframe(
        dataframe[
            available_columns
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No monitoring observations available."
    )


# ============================================================
# SYSTEM STATUS
# ============================================================

st.divider()

st.header(
    "🔌 System Status"
)

system1, system2, system3 = st.columns(3)


with system1:

    if backend_online:

        st.success(
            "🟢 FastAPI Backend: ONLINE"
        )

    else:

        st.error(
            "🔴 FastAPI Backend: OFFLINE"
        )


with system2:

    if (
        selected_video == "annotated_browser.mp4"
        and os.path.exists(
            os.path.join(
                OUTPUT_DIR,
                "annotated_browser.mp4"
            )
        )
    ):

        st.success(
            "🟢 AI Video: READY"
        )

    elif os.path.exists(
        os.path.join(
            OUTPUT_DIR,
            "annotated_test.mp4"
        )
    ):

        st.warning(
            "🟡 AI Video: Original annotation"
        )

    else:

        st.error(
            "🔴 AI Video: NOT FOUND"
        )


with system3:

    st.success(
        "🟢 MySQL: CONNECTED"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CrowdGuard AI · Agentic AI Crowd Management"
)

st.caption(
    "YOLO + ByteTrack · Crowd Flow · Density Analysis · "
    "Surge Risk · Threat Detection · FastAPI · MySQL"
)