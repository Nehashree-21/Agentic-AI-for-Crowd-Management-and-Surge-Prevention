import cv2

from ai.preprocessing.video_acquisition import (
    VideoAcquisition
)

from ai.tracking.person_tracker import (
    PersonTracker
)


class VideoAnnotator:

    def __init__(
        self,
        model_path="yolov8m.pt",
        confidence=0.20,
        image_size=1280
    ):

        self.tracker = PersonTracker(
            model_path=model_path,
            confidence=confidence,
            image_size=image_size
        )

    def process(
        self,
        input_path,
        output_path
    ):

        video = VideoAcquisition(
            input_path
        )

        video.open()

        info = video.get_video_info()

        width = info["width"]
        height = info["height"]
        fps = info["fps"]

        writer = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(
                *"mp4v"
            ),
            fps,
            (width, height)
        )

        frame_number = 0

        try:

            while True:

                success, frame = (
                    video.read_frame()
                )

                if not success:
                    break

                frame_number += 1

                people = (
                    self.tracker.track(
                        frame
                    )
                )

                # Draw detections
                for person in people:

                    x1, y1, x2, y2 = (
                        person["bbox"]
                    )

                    track_id = (
                        person["track_id"]
                    )

                    confidence = (
                        person["confidence"]
                    )

                    # Bounding box
                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    # Track label
                    label = (
                        f"ID {track_id} "
                        f"| {confidence:.2f}"
                    )

                    cv2.putText(
                        frame,
                        label,
                        (x1, max(y1 - 8, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 255, 0),
                        2
                    )

                # Header
                cv2.rectangle(
                    frame,
                    (0, 0),
                    (width, 55),
                    (10, 17, 30),
                    -1
                )

                cv2.putText(
                    frame,
                    "CROWDGUARD AI",
                    (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 255, 255),
                    2
                )

                # Crowd count
                count_text = (
                    f"People: {len(people)}"
                )

                cv2.putText(
                    frame,
                    count_text,
                    (width - 220, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 255),
                    2
                )

                writer.write(
                    frame
                )

        finally:

            video.release()
            writer.release()

        return output_path