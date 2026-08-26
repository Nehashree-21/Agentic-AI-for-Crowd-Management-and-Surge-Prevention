from pathlib import Path
from ultralytics import YOLO


class WeaponDetector:
    """
    Detects predefined weapon/threat classes using a
    separate YOLO model.
    """

    def __init__(
        self,
        model_path="weapon_model.pt",
        confidence=0.40,
        image_size=1280
    ):
        self.model_path = Path(model_path)
        self.confidence = confidence
        self.image_size = image_size
        self.model = None

        if not self.model_path.exists():
            print(
                f"WARNING: Threat model not found: "
                f"{self.model_path}"
            )
            print(
                "Threat detection is currently disabled."
            )
            return

        print(
            f"Loading threat detection model: "
            f"{self.model_path}"
        )

        self.model = YOLO(str(self.model_path))

    def detect(self, frame):
        """
        Detect weapons/threat objects in a frame.

        Returns:
            list of dictionaries containing:
            - class_id
            - class_name
            - confidence
            - bbox
        """

        if self.model is None:
            return []

        results = self.model.predict(
            frame,
            conf=self.confidence,
            imgsz=self.image_size,
            verbose=False
        )

        result = results[0]

        detections = []

        if result.boxes is None:
            return detections

        boxes = result.boxes

        coordinates = boxes.xyxy.cpu().tolist()
        confidences = boxes.conf.cpu().tolist()
        class_ids = boxes.cls.int().cpu().tolist()

        names = self.model.names

        for bbox, confidence, class_id in zip(
            coordinates,
            confidences,
            class_ids
        ):
            x1, y1, x2, y2 = bbox

            class_name = names[class_id]

            detections.append({
                "class_id": int(class_id),
                "class_name": str(class_name),
                "confidence": round(
                    float(confidence),
                    3
                ),
                "bbox": [
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                ]
            })

        return detections