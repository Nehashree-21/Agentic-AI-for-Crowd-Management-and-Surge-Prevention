from backend.models.monitoring import MonitoringStatus
from backend.database.mysql_service import get_connection


def get_monitoring_status() -> MonitoringStatus:

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                crowd_count,
                density,
                risk_score,
                risk_level,
                dominant_direction,
                flow_consistency
            FROM crowd_observations
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        if row is None:

            return MonitoringStatus(
                crowd_count=0,
                density="NORMAL",
                surge_risk="LOW",
                risk_score=0,
                threat_status="NO_THREAT",
                agent_decision="MONITOR",
                dominant_direction="STATIONARY",
                flow_consistency=0.0
            )

        risk_level = row["risk_level"]

        if risk_level == "CRITICAL":

            decision = (
                "IMMEDIATE_OPERATOR_ALERT"
            )

        elif risk_level == "WARNING":

            decision = (
                "MONITOR_AND_CONSIDER_REDIRECTION"
            )

        else:

            decision = (
                "CONTINUE_MONITORING"
            )

        return MonitoringStatus(
            crowd_count=row["crowd_count"],
            density=row["density"],
            surge_risk=risk_level,
            risk_score=row["risk_score"],
            threat_status="NO_THREAT",
            agent_decision=decision,
            dominant_direction=(
                row["dominant_direction"]
            ),
            flow_consistency=(
                row["flow_consistency"]
            )
        )

    finally:

        cursor.close()
        connection.close()


def update_monitoring_status(
    crowd_count,
    density,
    surge_risk,
    risk_score,
    threat_status,
    agent_decision,
    dominant_direction,
    flow_consistency
):
    """
    Compatibility function used by the
    CV monitoring pipeline.

    The actual persistent observation is
    stored separately in MySQL.
    """

    return MonitoringStatus(
        crowd_count=int(crowd_count),
        density=str(density),
        surge_risk=str(surge_risk),
        risk_score=int(risk_score),
        threat_status=str(threat_status),
        agent_decision=str(agent_decision),
        dominant_direction=str(
            dominant_direction
        ),
        flow_consistency=float(
            flow_consistency
        )
    )