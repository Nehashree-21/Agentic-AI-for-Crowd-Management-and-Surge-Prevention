from backend.models.status import CrowdStatus


def get_current_status() -> CrowdStatus:
    return CrowdStatus(
        crowd_count=0,
        density="NORMAL",
        surge_risk="LOW",
        threat_status="NO_THREAT",
        agent_decision="MONITOR",
    )