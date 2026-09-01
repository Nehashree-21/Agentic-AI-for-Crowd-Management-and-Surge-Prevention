from backend.services.monitoring_service import (
    update_monitoring_status
)


def update_from_crowd_analysis(
    crowd_count,
    density,
    risk,
    flow
):
    """
    Send crowd-analysis results to the
    FastAPI monitoring state.
    """

    return update_monitoring_status(
        crowd_count=int(crowd_count),

        density=str(
            density
        ),

        surge_risk=str(
            risk["risk_level"]
        ),

        risk_score=int(
            risk["risk_score"]
        ),

        # Threat detection will be connected
        # by the threat-detection module later.
        threat_status="NO_THREAT",

        # Agentic AI will replace this later.
        agent_decision=(
            get_basic_decision(
                risk["risk_level"]
            )
        ),

        dominant_direction=str(
            flow["dominant_direction"]
        ),

        flow_consistency=float(
            flow["flow_consistency"]
        )
    )


def get_basic_decision(
    risk_level
):

    if risk_level == "CRITICAL":
        return "IMMEDIATE_OPERATOR_ALERT"

    if risk_level == "WARNING":
        return "MONITOR_AND_CONSIDER_REDIRECTION"

    return "CONTINUE_MONITORING"