from ultralytics import YOLO


class PersonDetector:
    def __init__(
        self,
        model_name="yolov8m.pt",
        confidence=0.20,
        image_size=1536
    ):
        print(f"Loading YOLO model: {model_name}")

        self.model = YOLO(model_name)
        self.confidence = confidence
        self.image_size = image_size

    def detect(self, frame):
        """Detect people in a frame."""

        results = self.model(
            frame,
            conf=self.confidence,
            imgsz=self.image_size,
            classes=[0],
            verbose=False
        )

        result = results[0]

        boxes = []

        if result.boxes is not None:

            for box in result.boxes:

                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0])

                boxes.append({
                    "bbox": [
                        int(x1),
                        int(y1),
                        int(x2),
                        int(y2)
                    ],
                    "confidence": round(confidence, 3)
                })

        return boxes

    def count_people(self, frame):
        boxes = self.detect(frame)

        return len(boxes), boxes