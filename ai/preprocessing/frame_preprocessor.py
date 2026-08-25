import cv2
import numpy as np


class FramePreprocessor:
    def __init__(self, width=1280):
        self.width = width

    def resize(self, frame):
        """Resize frame while maintaining aspect ratio."""
        height, width = frame.shape[:2]

        if width <= self.width:
            return frame

        ratio = self.width / width
        new_height = int(height * ratio)

        return cv2.resize(
            frame,
            (self.width, new_height),
            interpolation=cv2.INTER_AREA
        )

    def denoise(self, frame):
        """Apply light noise reduction."""
        return cv2.GaussianBlur(frame, (3, 3), 0)

    def preprocess(self, frame):
        """Apply the complete preprocessing pipeline."""
        frame = self.resize(frame)
        frame = self.denoise(frame)

        return frame