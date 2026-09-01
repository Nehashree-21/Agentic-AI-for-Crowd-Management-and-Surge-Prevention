from pydantic import BaseModel


class CrowdStatus(BaseModel):
    crowd_count: int
    density: str
    surge_risk: str
    threat_status: str
    agent_decision: str