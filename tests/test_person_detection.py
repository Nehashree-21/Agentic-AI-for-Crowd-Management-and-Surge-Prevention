from ai.preprocessing.video_acquisition import VideoAcquisition
from ai.preprocessing.frame_preprocessor import FramePreprocessor
from ai.detection.person_detector import PersonDetector

from utils.visualization import draw_person_detections
import cv2
import os
VIDEO_PATH = "videos/test.mp4"


def main():
    print("Initializing components...")

    video = VideoAcquisition(VIDEO_PATH)
    preprocessor = FramePreprocessor(width=1280)
    detector = PersonDetector(
    model_name="yolov8m.pt",
    confidence=0.20,
    image_size=1280
)

    try:
        video.open()

        success, frame = video.read_frame()

        if not success:
            print("Could not read frame.")
            return

        count, people = detector.count_people(frame)
        output_frame = draw_person_detections(
    frame,
    people
)
        os.makedirs("outputs", exist_ok=True)

        output_path = "outputs/person_detection_result.jpg"
        cv2.imwrite(output_path, output_frame)

        print(f"\nDetection result saved to: {output_path}")

        print("\nPerson Detection Results")
        print("-" * 30)
        print(f"People detected: {count}")

        for index, person in enumerate(people, start=1):
            print(
                f"Person {index}: "
                f"Confidence={person['confidence']}, "
                f"Box={person['bbox']}"
            )

    finally:
        video.release()


if __name__ == "__main__":
    main()