from ai.preprocessing.video_acquisition import (
    VideoAcquisition
)

from ai.tracking.person_tracker import (
    PersonTracker
)

from ai.analysis.movement_analyzer import (
    MovementAnalyzer
)

from ai.analysis.zone_density_analyzer import (
    ZoneDensityAnalyzer
)

from ai.analysis.baseline_analyzer import (
    BaselineAnalyzer
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

    baseline_analyzer = (
        BaselineAnalyzer()
    )

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

            # Sample once per second
            if frame_number % 30 == 0:

                zones = (
                    zone_analyzer.analyze(
                        people
                    )
                )

                overall_density = (
                    zone_analyzer
                    .get_overall_density(
                        zones
                    )
                )

                average_displacement = (
                    movement_analyzer
                    .get_average_speed(
                        movements
                    )
                )

                baseline_analyzer.add_sample(
                    tracked_count=len(people),
                    average_displacement=
                        average_displacement,
                    overall_density=
                        overall_density
                )

        baseline = (
            baseline_analyzer.calculate()
        )

        print(
            "\n"
            + "=" * 55
        )

        print(
            "NORMAL CROWD BASELINE"
        )

        print(
            "=" * 55
        )

        print(
            f"Samples: "
            f"{baseline['sample_count']}"
        )

        print(
            "\nTracked People:"
        )

        print(
            f"  Mean: "
            f"{baseline['tracked_count']['mean']}"
        )

        print(
            f"  Std: "
            f"{baseline['tracked_count']['std']}"
        )

        print(
            f"  Minimum: "
            f"{baseline['tracked_count']['minimum']}"
        )

        print(
            f"  Maximum: "
            f"{baseline['tracked_count']['maximum']}"
        )

        print(
            "\nMovement:"
        )

        print(
            f"  Mean: "
            f"{baseline['movement']['mean']} "
            f"px/frame"
        )

        print(
            f"  Std: "
            f"{baseline['movement']['std']} "
            f"px/frame"
        )

        print(
            f"  Minimum: "
            f"{baseline['movement']['minimum']} "
            f"px/frame"
        )

        print(
            f"  Maximum: "
            f"{baseline['movement']['maximum']} "
            f"px/frame"
        )

        print(
            "\nDensity:"
        )

        print(
            f"  Mean level: "
            f"{baseline['density']['mean']}"
        )

        print(
            f"  Std: "
            f"{baseline['density']['std']}"
        )

        print(
            "=" * 55
        )

    finally:

        video.release()


if __name__ == "__main__":
    main()