from typing import Dict, List


class ThreatAnalyzer:

    def analyze(
        self,
        detections: List[Dict]
    ) -> Dict:

        if not detections:
            return {
                "threat_detected": False,
                "threat_confidence": 0.0,
                "threat_classes": [],
                "detections": []
            }

        threat_classes = sorted(
            set(
                detection["class_name"]
                for detection in detections
            )
        )

        threat_confidence = max(
            detection["confidence"]
            for detection in detections
        )

        return {
            "threat_detected": True,
            "threat_confidence": threat_confidence,
            "threat_classes": threat_classes,
            "detections": detections
        }