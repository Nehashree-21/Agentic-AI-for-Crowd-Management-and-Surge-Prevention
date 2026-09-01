from ai.visualization.video_annotator import (
    VideoAnnotator
)


INPUT_VIDEO = "videos/test.mp4"

OUTPUT_VIDEO = (
    "outputs/annotated_test.mp4"
)


def main():

    annotator = VideoAnnotator(
        model_path="yolov8m.pt",
        confidence=0.20,
        image_size=1280
    )

    result = annotator.process(
        INPUT_VIDEO,
        OUTPUT_VIDEO
    )

    print()
    print("=" * 50)
    print("ANNOTATED VIDEO CREATED")
    print("=" * 50)
    print(
        f"Output: {result}"
    )


if __name__ == "__main__":
    main()