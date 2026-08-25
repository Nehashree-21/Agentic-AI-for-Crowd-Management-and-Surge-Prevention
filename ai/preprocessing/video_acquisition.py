import cv2


class VideoAcquisition:
    def __init__(self, source):
        self.source = source
        self.cap = None

    def open(self):
        """Open the video source."""
        self.cap = cv2.VideoCapture(self.source)

        if not self.cap.isOpened():
            raise ValueError(f"Could not open video source: {self.source}")

    def get_video_info(self):
        """Return basic information about the video."""
        if self.cap is None:
            raise RuntimeError("Video source is not opened.")

        return {
            "fps": self.cap.get(cv2.CAP_PROP_FPS),
            "width": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "total_frames": int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        }

    def read_frame(self):
        """Read one frame from the video."""
        if self.cap is None:
            raise RuntimeError("Video source is not opened.")

        return self.cap.read()

    def release(self):
        """Release the video source."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None