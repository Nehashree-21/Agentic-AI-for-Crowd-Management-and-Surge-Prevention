from ai.agent.decision_agent import CrowdDecisionAgent


def print_result(title, result):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(f"Risk Level:       {result['risk_level']}")
    print(f"Risk Score:       {result['risk_score']}")
    print(f"Decision:         {result['decision']}")
    print(f"Alert Priority:   {result['alert_priority']}")
    print(f"Recommended:      {result['recommended_action']}")

    print("\nReasons:")

    for reason in result["reasons"]:
        print(f"  - {reason}")


def main():

    agent = CrowdDecisionAgent()

    # -------------------------------------------------
    # TEST 1 — Normal situation
    # -------------------------------------------------

    result = agent.evaluate(
        crowd_count=25,
        density="MEDIUM",
        movement=2.5,
        flow="RIGHT",
        flow_consistency=40,
        movement_change=5,
        surge_risk_score=10,
        surge_risk_level="LOW"
    )

    print_result(
        "TEST 1 — NORMAL CROWD",
        result
    )

    # -------------------------------------------------
    # TEST 2 — Warning situation
    # -------------------------------------------------

    result = agent.evaluate(
        crowd_count=32,
        density="HIGH",
        movement=3.7,
        flow="UP",
        flow_consistency=50,
        movement_change=22,
        surge_risk_score=40,
        surge_risk_level="WARNING"
    )

    print_result(
        "TEST 2 — WARNING CROWD",
        result
    )

    # -------------------------------------------------
    # TEST 3 — Critical surge
    # -------------------------------------------------

    result = agent.evaluate(
        crowd_count=29,
        density="MEDIUM",
        movement=6.9,
        flow="UP",
        flow_consistency=88.89,
        movement_change=315.66,
        surge_risk_score=75,
        surge_risk_level="CRITICAL"
    )

    print_result(
        "TEST 3 — CRITICAL SURGE",
        result
    )

    # -------------------------------------------------
    # TEST 4 — Potential threat
    # -------------------------------------------------

    result = agent.evaluate(
        crowd_count=30,
        density="HIGH",
        movement=3.5,
        flow="RIGHT",
        flow_consistency=60,
        movement_change=20,
        surge_risk_score=35,
        surge_risk_level="WARNING",
        threat_detected=True,
        threat_confidence=0.87,
        threat_classes=["weapon"]
    )

    print_result(
        "TEST 4 — POTENTIAL THREAT",
        result
    )


if __name__ == "__main__":
    main()