from fastapi import FastAPI

app = FastAPI(
    title="Agentic AI Crowd Management API",
    description="Backend API for crowd monitoring, surge prevention, and threat detection.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Agentic AI Crowd Management API is running successfully!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }