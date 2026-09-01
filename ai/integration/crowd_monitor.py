from backend.database.observation_service import (
    save_crowd_observation
)

from backend.database.alert_service import (
    save_alert
)

from ai.preprocessing.video_acquisition import (
    VideoAcquisition
)

from ai.tracking.person_tracker import (
    PersonTracker
)

from ai.analysis.movement_analyzer import (
    MovementAnalyzer
)

from ai.analysis.crowd_flow_analyzer import (
    CrowdFlowAnalyzer
)

from ai.analysis.zone_density_analyzer import (
    ZoneDensityAnalyzer
)

from ai.analysis.surge_risk_engine import (
    SurgeRiskEngine
)

from ai.integration.monitoring_bridge import (
    update_from_crowd_analysis
)


class CrowdMonitor:

    def __init__(
        self,
        video_path
    ):

        self.video = VideoAcquisition(
            video_path
        )

        self.tracker = PersonTracker(
            model_path="yolov8m.pt",
            confidence=0.20,
            image_size=1280
        )

        self.movement_analyzer = (
            MovementAnalyzer()
        )

        self.flow_analyzer = (
            CrowdFlowAnalyzer()
        )

        self.risk_engine = (
            SurgeRiskEngine()
        )

        self.zone_analyzer = None

        # Prevent duplicate alerts
        self.last_alert_level = None

    def run(self):

        self.video.open()

        info = (
            self.video.get_video_info()
        )

        self.zone_analyzer = (
            ZoneDensityAnalyzer(
                frame_width=info["width"],
                frame_height=info["height"]
            )
        )

        frame_number = 0

        try:

            while True:

                success, frame = (
                    self.video.read_frame()
                )

                if not success:
                    break

                frame_number += 1

                people = (
                    self.tracker.track(
                        frame
                    )
                )

                movements = (
                    self.movement_analyzer.update(
                        people
                    )
                )

                # Analyze once per second
                if frame_number % 30 == 0:

                    flow = (
                        self.flow_analyzer.analyze(
                            movements
                        )
                    )

                    zones = (
                        self.zone_analyzer.analyze(
                            people
                        )
                    )

                    density = (
                        self.zone_analyzer
                        .get_overall_density(
                            zones
                        )
                    )

                    risk = (
                        self.risk_engine.calculate_score(
                            average_displacement=
                                flow[
                                    "average_displacement"
                                ],

                            density_level=
                                density,

                            flow_consistency=
                                flow[
                                    "flow_consistency"
                                ],

                            movement_change=
                                flow[
                                    "movement_change"
                                ]
                        )
                    )

                    # --------------------------------
                    # Update FastAPI monitoring state
                    # --------------------------------

                    status = (
                        update_from_crowd_analysis(
                            crowd_count=len(
                                people
                            ),

                            density=density,

                            risk=risk,

                            flow=flow
                        )
                    )

                    # --------------------------------
                    # Save observation to MySQL
                    # --------------------------------

                    save_crowd_observation(
                        crowd_count=len(
                            people
                        ),

                        density=density,

                        average_movement=
                            flow[
                                "average_displacement"
                            ],

                        dominant_direction=
                            flow[
                                "dominant_direction"
                            ],

                        flow_consistency=
                            flow[
                                "flow_consistency"
                            ],

                        risk_score=
                            risk[
                                "risk_score"
                            ],

                        risk_level=
                            risk[
                                "risk_level"
                            ]
                    )

                    # --------------------------------
                    # Automatic surge alert
                    # --------------------------------

                    current_risk_level = (
                        risk["risk_level"]
                    )

                    if current_risk_level in [
                        "WARNING",
                        "CRITICAL"
                    ]:

                        # Only create a new alert
                        # when the risk level changes.
                        if (
                            current_risk_level
                            != self.last_alert_level
                        ):

                            save_alert(
                                alert_type="SURGE",

                                severity=
                                    current_risk_level,

                                message=(
                                    "Abnormal crowd "
                                    "movement detected. "
                                    f"Risk score: "
                                    f"{risk['risk_score']}/100. "
                                    f"Direction: "
                                    f"{flow['dominant_direction']}. "
                                    f"Flow consistency: "
                                    f"{flow['flow_consistency']}%."
                                ),

                                confidence=(
                                    risk["risk_score"]
                                    / 100
                                ),

                                status="ACTIVE"
                            )

                            self.last_alert_level = (
                                current_risk_level
                            )

                    else:

                        # Reset so that a future
                        # WARNING/CRITICAL event
                        # can generate a new alert.
                        self.last_alert_level = None

                    # --------------------------------
                    # Console output
                    # --------------------------------

                    print(
                        f"\nFrame {frame_number}"
                    )

                    print(
                        f"Crowd: "
                        f"{status.crowd_count}"
                    )

                    print(
                        f"Density: "
                        f"{status.density}"
                    )

                    print(
                        f"Risk: "
                        f"{status.risk_score}/100 "
                        f"({status.surge_risk})"
                    )

                    print(
                        f"Flow: "
                        f"{status.dominant_direction}"
                    )

        finally:

            self.video.release()