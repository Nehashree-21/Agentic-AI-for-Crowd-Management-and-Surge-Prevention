from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction


class CrowdDetector:
    def __init__(
        self,
        model_path="yolov8m.pt",
        confidence=0.20
    ):
        print(f"Loading tiled YOLO model: {model_path}")

        self.model = AutoDetectionModel.from_pretrained(
            model_type="ultralytics",
            model_path=model_path,
            confidence_threshold=confidence,
            device="cpu"
        )

    def detect(self, frame):
        """
        Detect people using sliced/tiled inference.
        """

        result = get_sliced_prediction(
            frame,
            self.model,
            slice_height=512,
            slice_width=512,
            overlap_height_ratio=0.20,
            overlap_width_ratio=0.20,
            verbose=0
        )

        people = []

        for prediction in result.object_prediction_list:

            # COCO class 0 = person
            if prediction.category.id != 0:
                continue

            bbox = prediction.bbox.to_xyxy()
            confidence = prediction.score.value

            people.append({
                "bbox": [
                    int(bbox[0]),
                    int(bbox[1]),
                    int(bbox[2]),
                    int(bbox[3])
                ],
                "confidence": round(float(confidence), 3)
            })

        return people

    def count_people(self, frame):
        people = self.detect(frame)
        return len(people), people