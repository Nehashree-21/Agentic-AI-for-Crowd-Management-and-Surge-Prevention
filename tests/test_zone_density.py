from ai.preprocessing.video_acquisition import (
    VideoAcquisition
)

from ai.tracking.person_tracker import (
    PersonTracker
)

from ai.analysis.zone_density_analyzer import (
    ZoneDensityAnalyzer
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

    try:

        video.open()

        info = (
            video.get_video_info()
        )

        analyzer = (
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

            # Analyze once every second
            if frame_number % 30 == 0:

                zones = analyzer.analyze(
                    people
                )

                overall = (
                    analyzer.get_overall_density(
                        zones
                    )
                )

                print(
                    f"\n{'=' * 45}"
                )

                print(
                    f"Frame: {frame_number}"
                )

                print(
                    f"Tracked people: "
                    f"{len(people)}"
                )

                print(
                    f"Overall density: "
                    f"{overall}"
                )

                print(
                    "\nZone information:"
                )

                for zone, data in (
                    zones.items()
                ):

                    print(
                        f"Zone {zone}: "
                        f"{data['count']} people | "
                        f"{data['percentage']}% | "
                        f"{data['density']}"
                    )

    finally:

        video.release()


if __name__ == "__main__":
    main()