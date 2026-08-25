from ai.preprocessing.video_acquisition import VideoAcquisition
from ai.tracking.person_tracker import PersonTracker

import cv2
import os


VIDEO_PATH = "videos/test.mp4"


def main():

    video = VideoAcquisition(VIDEO_PATH)

    tracker = PersonTracker(
        model_path="yolov8m.pt",
        confidence=0.20,
        image_size=1280
    )

    os.makedirs("outputs", exist_ok=True)

    output_path = "outputs/tracking_result.mp4"

    writer = None

    try:

        video.open()

        info = video.get_video_info()

        fps = info["fps"]
        width = info["width"]
        height = info["height"]

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        writer = cv2.VideoWriter(
            output_path,
            fourcc,
            fps,
            (width, height)
        )

        frame_number = 0

        while True:

            success, frame = video.read_frame()

            if not success:
                break

            frame_number += 1

            people = tracker.track(frame)

            for person in people:

                track_id = person["track_id"]

                x1, y1, x2, y2 = person["bbox"]

                confidence = person["confidence"]

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                label = (
                    f"ID {track_id} "
                    f"{confidence:.2f}"
                )

                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            writer.write(frame)

            if frame_number % 30 == 0:

                print(
                    f"Frame {frame_number}: "
                    f"{len(people)} tracked people"
                )

        print("\nTracking completed.")
        print(
            f"Result saved to: {output_path}"
        )

    finally:

        video.release()

        if writer is not None:
            writer.release()


if __name__ == "__main__":
    main()