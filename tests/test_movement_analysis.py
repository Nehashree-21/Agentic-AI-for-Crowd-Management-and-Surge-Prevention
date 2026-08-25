from ai.preprocessing.video_acquisition import VideoAcquisition
from ai.tracking.person_tracker import PersonTracker
from ai.analysis.movement_analyzer import MovementAnalyzer


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

    analyzer = MovementAnalyzer()

    try:

        video.open()

        frame_number = 0

        while True:

            success, frame = video.read_frame()

            if not success:
                break

            frame_number += 1

            people = tracker.track(
                frame
            )

            movements = analyzer.update(
                people
            )

            if frame_number % 30 == 0:

                average_speed = (
                    analyzer.get_average_speed(
                        movements
                    )
                )

                print(
                    f"\nFrame {frame_number}"
                )

                print(
                    f"Tracked people: "
                    f"{len(people)}"
                )

                print(
                    f"Average displacement: "
                    f"{average_speed} px/frame"
                )

                for movement in movements[:5]:

                    print(
                        f"ID {movement['track_id']} | "
                        f"Direction: "
                        f"{movement['direction']} | "
                        f"Displacement: "
                        f"{movement['displacement']}"
                    )

    finally:

        video.release()


if __name__ == "__main__":
    main()