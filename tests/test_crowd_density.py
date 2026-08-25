from ai.preprocessing.video_acquisition import VideoAcquisition
from ai.density.density_estimator import CrowdDensityEstimator

import cv2
import numpy as np
import os


VIDEO_PATH = "videos/test.mp4"


def create_heatmap(density_map, frame):

    density_map = np.maximum(
        density_map,
        0
    )

    normalized = cv2.normalize(
        density_map,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    heatmap = cv2.resize(
        normalized.astype(np.uint8),
        (
            frame.shape[1],
            frame.shape[0]
        )
    )

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    overlay = cv2.addWeighted(
        frame,
        0.6,
        heatmap,
        0.4,
        0
    )

    return overlay


def main():

    video = VideoAcquisition(
        VIDEO_PATH
    )

    estimator = CrowdDensityEstimator()

    try:

        video.open()

        success, frame = video.read_frame()

        if not success:

            print(
                "Could not read frame."
            )

            return

        print(
            "\nRunning crowd-density estimation..."
        )

        count, density_map = (
            estimator.estimate(frame)
        )

        print(
            f"\nEstimated crowd count: "
            f"{count:.2f}"
        )

        print(
            f"Density map shape: "
            f"{density_map.shape}"
        )

        heatmap = create_heatmap(
            density_map,
            frame
        )

        os.makedirs(
            "outputs",
            exist_ok=True
        )

        output_path = (
            "outputs/crowd_density_heatmap.jpg"
        )

        cv2.imwrite(
            output_path,
            heatmap
        )

        print(
            f"Heatmap saved to: "
            f"{output_path}"
        )

    finally:

        video.release()


if __name__ == "__main__":
    main()