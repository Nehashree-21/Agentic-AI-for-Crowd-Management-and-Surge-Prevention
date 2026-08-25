import cv2


def draw_person_detections(frame, people):
    """Draw person bounding boxes and confidence scores."""

    output = frame.copy()

    for index, person in enumerate(people, start=1):
        x1, y1, x2, y2 = person["bbox"]
        confidence = person["confidence"]

        cv2.rectangle(
            output,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        label = f"Person {index}: {confidence:.2f}"

        cv2.putText(
            output,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    return output