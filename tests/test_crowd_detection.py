from ai.preprocessing.video_acquisition import VideoAcquisition
from ai.detection.crowd_detector import CrowdDetector
from utils.visualization import draw_person_detections

import cv2
import os


VIDEO_PATH = "videos/test.mp4"


def main():

    video = VideoAcquisition(VIDEO_PATH)

    detector = CrowdDetector(
        model_path="yolov8m.pt",
        confidence=0.20
    )

    try:
        video.open()

        success, frame = video.read_frame()

        if not success:
            print("Could not read frame.")
            return

        count, people = detector.count_people(frame)

        print("\nTiled Crowd Detection Results")
        print("-" * 35)
        print(f"People detected: {count}")

        for index, person in enumerate(people, start=1):
            print(
                f"Person {index}: "
                f"Confidence={person['confidence']}, "
                f"Box={person['bbox']}"
            )

        output_frame = draw_person_detections(
            frame,
            people
        )

        os.makedirs("outputs", exist_ok=True)

        output_path = "outputs/tiled_crowd_detection.jpg"

        cv2.imwrite(
            output_path,
            output_frame
        )

        print(
            f"\nDetection result saved to: {output_path}"
        )

    finally:
        video.release()


if __name__ == "__main__":
    main()