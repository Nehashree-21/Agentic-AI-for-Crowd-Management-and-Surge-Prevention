import cv2

from ai.threat.weapon_detector import WeaponDetector


VIDEO_PATH = "data/videos/crowd_video.mp4"


def main():

    detector = WeaponDetector(
        model_path="weapon_model.pt",
        confidence=0.40,
        image_size=1280
    )

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("Could not open video.")
        return

    frame_number = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_number += 1

        detections = detector.detect(frame)

        if detections:

            print("\n" + "=" * 50)
            print(f"Frame: {frame_number}")
            print("Threat detections:")

            for detection in detections:

                print(
                    f"Class: {detection['class_name']} | "
                    f"Confidence: {detection['confidence']} | "
                    f"Box: {detection['bbox']}"
                )

    cap.release()

    print("\nThreat detection test completed.")


if __name__ == "__main__":
    main()