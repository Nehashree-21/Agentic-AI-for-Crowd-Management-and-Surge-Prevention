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

    try:

        video.open()

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

            flow = (
                flow_analyzer.analyze(
                    movements
                )
            )

            # Analyze once every second
            if frame_number % 30 == 0:

                print(
                    f"\n{'=' * 45}"
                )

                print(
                    f"Frame: {frame_number}"
                )

                print(
                    f"Tracked people: "
                    f"{flow['total_tracked']}"
                )

                print(
                    f"Average displacement: "
                    f"{flow['average_displacement']} "
                    f"px/frame"
                )

                print(
                    f"Dominant direction: "
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
                    "Direction distribution:"
                )

                for direction, percentage in (
                    flow[
                        "direction_distribution"
                    ].items()
                ):

                    print(
                        f"  {direction}: "
                        f"{percentage}%"
                    )

    finally:

        video.release()


if __name__ == "__main__":
    main()