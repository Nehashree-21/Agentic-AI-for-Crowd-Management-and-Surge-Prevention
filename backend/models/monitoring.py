from pydantic import BaseModel


class MonitoringStatus(BaseModel):
    crowd_count: int
    density: str
    surge_risk: str
    risk_score: int
    threat_status: str
    agent_decision: str
    dominant_direction: str
    flow_consistency: float