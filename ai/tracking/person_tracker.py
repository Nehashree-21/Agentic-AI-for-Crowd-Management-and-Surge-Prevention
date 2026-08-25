from ultralytics import YOLO


class PersonTracker:
    def __init__(
        self,
        model_path="yolov8m.pt",
        confidence=0.20,
        image_size=1280
    ):
        print(f"Loading tracking model: {model_path}")

        self.model = YOLO(model_path)
        self.confidence = confidence
        self.image_size = image_size

    def track(self, frame):
        """
        Detect and track people in the current frame.
        ByteTrack assigns persistent IDs.
        """

        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],
            conf=self.confidence,
            imgsz=self.image_size,
            verbose=False
        )

        result = results[0]

        tracked_people = []

        if result.boxes is None:
            return tracked_people

        boxes = result.boxes

        if boxes.id is None:
            return tracked_people

        track_ids = boxes.id.int().cpu().tolist()
        coordinates = boxes.xyxy.cpu().tolist()
        confidences = boxes.conf.cpu().tolist()

        for track_id, bbox, confidence in zip(
            track_ids,
            coordinates,
            confidences
        ):
            x1, y1, x2, y2 = bbox

            tracked_people.append({
                "track_id": int(track_id),
                "bbox": [
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                ],
                "confidence": round(
                    float(confidence),
                    3
                )
            })

        return tracked_people