from typing import Dict, List


class CrowdDecisionAgent:
    """
    Agentic decision layer for crowd management.

    Receives structured observations from:
    - Crowd counting
    - Density analysis
    - Crowd flow analysis
    - Surge-risk analysis
    - Threat detection

    Produces:
    - Risk level
    - Decision
    - Recommended action
    - Alert priority
    """

    def __init__(self):
        self.risk_levels = {
            "NORMAL": 0,
            "WARNING": 1,
            "CRITICAL": 2
        }

    def evaluate(
        self,
        crowd_count: int,
        density: str,
        movement: float,
        flow: str,
        flow_consistency: float,
        movement_change: float,
        surge_risk_score: float,
        surge_risk_level: str,
        threat_detected: bool = False,
        threat_confidence: float = 0.0,
        threat_classes: List[str] | None = None
    ) -> Dict:

        threat_classes = threat_classes or []

        reasons = []

        # -------------------------------------------------
        # 1. Start with surge-risk result
        # -------------------------------------------------

        risk_score = float(surge_risk_score)

        if surge_risk_level.upper() == "CRITICAL":
            risk_level = "CRITICAL"
            reasons.append("Critical surge-risk detected.")

        elif surge_risk_level.upper() == "WARNING":
            risk_level = "WARNING"
            reasons.append("Elevated crowd-risk detected.")

        else:
            risk_level = "NORMAL"

        # -------------------------------------------------
        # 2. Density assessment
        # -------------------------------------------------

        density_upper = density.upper()

        if density_upper == "HIGH":
            risk_score += 15
            reasons.append("High crowd density detected.")

        elif density_upper == "MEDIUM":
            risk_score += 5

        # -------------------------------------------------
        # 3. Abnormal movement
        # -------------------------------------------------

        if movement_change >= 50:
            risk_score += 15
            reasons.append("Large positive movement change detected.")

        elif movement_change >= 25:
            risk_score += 8
            reasons.append("Positive movement change is elevated.")

        # -------------------------------------------------
        # 4. Crowd flow consistency
        # -------------------------------------------------

        if flow_consistency >= 80 and movement >= 5:
            risk_score += 15
            reasons.append(
                f"Strong directional crowd movement detected ({flow})."
            )

        # -------------------------------------------------
        # 5. Threat detection
        # -------------------------------------------------

        if threat_detected:

            # Threat detection gets priority.
            risk_level = "CRITICAL"

            risk_score = max(risk_score, 90)

            reasons.append(
                "Potential threat detected and requires human verification."
            )

        # -------------------------------------------------
        # 6. Clamp score
        # -------------------------------------------------

        risk_score = min(100, max(0, round(risk_score)))

        # -------------------------------------------------
        # 7. Final risk level
        # -------------------------------------------------

        if threat_detected:
            risk_level = "CRITICAL"

        elif risk_score >= 70:
            risk_level = "CRITICAL"

        elif risk_score >= 40:
            risk_level = "WARNING"

        else:
            risk_level = "NORMAL"

        # -------------------------------------------------
        # 8. Agent decision
        # -------------------------------------------------

        if risk_level == "NORMAL":

            decision = "CONTINUE_MONITORING"

            action = (
                "Continue normal monitoring. "
                "No immediate intervention required."
            )

            alert_priority = "LOW"

        elif risk_level == "WARNING":

            decision = "NOTIFY_OPERATOR"

            action = (
                "Notify the operator and consider crowd "
                "redirection or flow management."
            )

            alert_priority = "MEDIUM"

        else:

            if threat_detected:

                decision = "SECURITY_VERIFICATION"

                action = (
                    "Immediately notify security personnel. "
                    "Potential threat requires human verification."
                )

            else:

                decision = "IMMEDIATE_OPERATOR_ALERT"

                action = (
                    "Immediately alert the operator and initiate "
                    "crowd-management intervention."
                )

            alert_priority = "HIGH"

        # -------------------------------------------------
        # 9. Return structured agent output
        # -------------------------------------------------

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "decision": decision,
            "recommended_action": action,
            "alert_priority": alert_priority,

            "observations": {
                "crowd_count": crowd_count,
                "density": density,
                "movement": round(float(movement), 2),
                "flow": flow,
                "flow_consistency": round(
                    float(flow_consistency), 2
                ),
                "movement_change": round(
                    float(movement_change), 2
                ),
                "surge_risk_score": surge_risk_score,
                "surge_risk_level": surge_risk_level,
                "threat_detected": threat_detected,
                "threat_confidence": round(
                    float(threat_confidence), 3
                ),
                "threat_classes": threat_classes
            },

            "reasons": reasons
        }