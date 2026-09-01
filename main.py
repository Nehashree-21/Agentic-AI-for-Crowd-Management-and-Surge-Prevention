from fastapi import FastAPI
from backend.database.alert_service import get_recent_alerts
from backend.services.observation_service import (
    get_recent_observations
)
from backend.services.monitoring_service import (
    get_monitoring_status
)


app = FastAPI(
    title="Agentic AI Crowd Management API",
    description=(
        "Backend API for crowd monitoring, "
        "surge prevention, and threat detection."
    ),
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message":
        "Agentic AI Crowd Management API is running successfully!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }



@app.get("/api/status")
def get_status():
    return get_monitoring_status()

@app.get("/api/observations")
def get_observations(limit: int = 20):
    return {
        "observations": get_recent_observations(
            limit
        )
    }
@app.get("/api/alerts")
def get_alerts(limit: int = 20):
    return {
        "alerts": get_recent_alerts(limit)
    }