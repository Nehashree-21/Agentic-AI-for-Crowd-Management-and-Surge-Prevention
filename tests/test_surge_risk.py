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


VIDEO_PATH = "videos/test.mp4"


def main():

    video = VideoAcquisition(
        VIDEO_PATH
    )

    tracker = PersonTracker(
        model_path="yolov8m.pt",
        confidence=0.20,
        image_size=1280
    )

    movement_analyzer = (
        MovementAnalyzer()
    )

    flow_analyzer = (
        CrowdFlowAnalyzer()
    )

    risk_engine = SurgeRiskEngine()

    try:

        video.open()

        info = (
            video.get_video_info()
        )

        zone_analyzer = (
            ZoneDensityAnalyzer(
                frame_width=info["width"],
                frame_height=info["height"]
            )
        )

        frame_number = 0

        while True:

            success, frame = (
                video.read_frame()
            )

            if not success:
                break

            frame_number += 1

            people = tracker.track(
                frame
            )

            movements = (
                movement_analyzer.update(
                    people
                )
            )

            if frame_number % 30 == 0:

                flow = (
                    flow_analyzer.analyze(
                        movements
                    )
                )

                zones = (
                    zone_analyzer.analyze(
                        people
                    )
                )

                density = (
                    zone_analyzer
                    .get_overall_density(
                        zones
                    )
                )

                risk = (
                    risk_engine.calculate_score(
                        average_displacement=
                            flow[
                                "average_displacement"
                            ],

                        density_level=density,

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

                print(
                    "\n"
                    + "=" * 55
                )

                print(
                    f"Frame: {frame_number}"
                )

                print(
                    f"Tracked people: "
                    f"{len(people)}"
                )

                print(
                    f"Density: {density}"
                )

                print(
                    f"Movement: "
                    f"{flow['average_displacement']} "
                    f"px/frame"
                )

                print(
                    f"Flow: "
                    f"{flow['dominant_direction']}"
                )

                print(
                    f"Flow consistency: "
                    f"{flow['flow_consistency']}%"
                )

                print(
                    f"Movement change: "
                    f"{flow['movement_change']}%"
                )

                print(
                    "\nRisk Analysis"
                )

                print(
                    f"Risk score: "
                    f"{risk['risk_score']}/100"
                )

                print(
                    f"Risk level: "
                    f"{risk['risk_level']}"
                )

                print(
                    f"Movement Z-score: "
                    f"{risk['movement_z_score']}"
                )

                print(
                    f"Density Z-score: "
                    f"{risk['density_z_score']}"
                )

    finally:

        video.release()


if __name__ == "__main__":
    main()