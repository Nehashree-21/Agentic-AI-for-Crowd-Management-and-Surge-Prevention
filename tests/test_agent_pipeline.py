import cv2

from ai.tracking.person_tracker import PersonTracker
from ai.analysis.movement_analyzer import MovementAnalyzer
from ai.analysis.crowd_flow_analyzer import CrowdFlowAnalyzer
from ai.analysis.zone_density_analyzer import ZoneDensityAnalyzer
from ai.analysis.surge_risk_engine import SurgeRiskEngine
from ai.agent.decision_agent import CrowdDecisionAgent


VIDEO_PATH = "videos/test.mp4"

MODEL_PATH = "yolov8m.pt"

FRAME_INTERVAL = 30


def main():

    print("=" * 70)
    print("AGENTIC CROWD MANAGEMENT - FULL PIPELINE TEST")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Open video
    # --------------------------------------------------

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print(f"\nERROR: Could not open video: {VIDEO_PATH}")
        return

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    print(f"\nVideo: {VIDEO_PATH}")
    print(f"Resolution: {width} x {height}")
    print(f"FPS: {fps}")
    print(f"Total frames: {total_frames}")

    # --------------------------------------------------
    # 2. Initialize AI modules
    # --------------------------------------------------

    tracker = PersonTracker(
        model_path=MODEL_PATH,
        confidence=0.20,
        image_size=1280
    )

    movement_analyzer = MovementAnalyzer()

    flow_analyzer = CrowdFlowAnalyzer()

    density_analyzer = ZoneDensityAnalyzer(
        frame_width=width,
        frame_height=height
    )

    surge_engine = SurgeRiskEngine()

    decision_agent = CrowdDecisionAgent()

    # --------------------------------------------------
    # 3. Process video
    # --------------------------------------------------

    frame_number = 0

    try:

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame_number += 1

            # ------------------------------------------
            # Process every FRAME_INTERVAL frames
            # ------------------------------------------

            if frame_number % FRAME_INTERVAL != 0:
                continue

            # ------------------------------------------
            # PERSON TRACKING
            # ------------------------------------------

            people = tracker.track(frame)

            crowd_count = len(people)

            # ------------------------------------------
            # MOVEMENT ANALYSIS
            # ------------------------------------------

            movements = movement_analyzer.update(
                people
            )

            # ------------------------------------------
            # CROWD FLOW
            # ------------------------------------------

            flow_result = flow_analyzer.analyze(
                movements
            )

            # ------------------------------------------
            # ZONE DENSITY
            # ------------------------------------------

            zone_results = density_analyzer.analyze(
                people
            )

            overall_density = (
                density_analyzer.get_overall_density(
                    zone_results
                )
            )

            # ------------------------------------------
            # SURGE RISK
            # ------------------------------------------

            surge_result = surge_engine.calculate_score(

                average_displacement=(
                    flow_result[
                        "average_displacement"
                    ]
                ),

                density_level=overall_density,

                flow_consistency=(
                    flow_result[
                        "flow_consistency"
                    ]
                ),

                movement_change=(
                    flow_result[
                        "movement_change"
                    ]
                )
            )

            # ------------------------------------------
            # AGENT DECISION
            # ------------------------------------------

            agent_result = decision_agent.evaluate(

                crowd_count=crowd_count,

                density=overall_density,

                movement=(
                    flow_result[
                        "average_displacement"
                    ]
                ),

                flow=(
                    flow_result[
                        "dominant_direction"
                    ]
                ),

                flow_consistency=(
                    flow_result[
                        "flow_consistency"
                    ]
                ),

                movement_change=(
                    flow_result[
                        "movement_change"
                    ]
                ),

                surge_risk_score=(
                    surge_result[
                        "risk_score"
                    ]
                ),

                surge_risk_level=(
                    surge_result[
                        "risk_level"
                    ]
                ),

                # Threat detector will be connected
                # in a later step.
                threat_detected=False,

                threat_confidence=0.0,

                threat_classes=[]
            )

            # ------------------------------------------
            # DISPLAY RESULTS
            # ------------------------------------------

            print("\n" + "=" * 70)

            print(
                f"FRAME {frame_number}"
            )

            print("=" * 70)

            print(
                f"Crowd count:        {crowd_count}"
            )

            print(
                f"Density:             {overall_density}"
            )

            print(
                f"Movement:            "
                f"{flow_result['average_displacement']} px/frame"
            )

            print(
                f"Flow:                "
                f"{flow_result['dominant_direction']}"
            )

            print(
                f"Flow consistency:    "
                f"{flow_result['flow_consistency']}%"
            )

            print(
                f"Movement change:     "
                f"{flow_result['movement_change']}%"
            )

            print(
                f"Surge risk score:    "
                f"{surge_result['risk_score']}/100"
            )

            print(
                f"Surge risk level:    "
                f"{surge_result['risk_level']}"
            )

            print("\n🤖 AGENT DECISION")

            print(
                f"Agent risk level:    "
                f"{agent_result['risk_level']}"
            )

            print(
                f"Agent risk score:    "
                f"{agent_result['risk_score']}/100"
            )

            print(
                f"Decision:            "
                f"{agent_result['decision']}"
            )

            print(
                f"Alert priority:      "
                f"{agent_result['alert_priority']}"
            )

            print(
                f"Recommended action:  "
                f"{agent_result['recommended_action']}"
            )

            if agent_result["reasons"]:

                print("\nReasons:")

                for reason in agent_result["reasons"]:
                    print(
                        f"  - {reason}"
                    )

    finally:

        cap.release()

        print("\n" + "=" * 70)
        print("PIPELINE TEST COMPLETE")
        print("=" * 70)


if __name__ == "__main__":
    main()