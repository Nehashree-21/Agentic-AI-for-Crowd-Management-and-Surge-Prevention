from ai.preprocessing.video_acquisition import VideoAcquisition
from ai.preprocessing.frame_preprocessor import FramePreprocessor


VIDEO_PATH = "videos/test.mp4"


def main():
    video = VideoAcquisition(VIDEO_PATH)
    preprocessor = FramePreprocessor(width=1280)

    try:
        video.open()
        info = video.get_video_info()

        print("\nVideo opened successfully!\n")
        print(f"FPS: {info['fps']}")
        print(f"Width: {info['width']}")
        print(f"Height: {info['height']}")
        print(f"Total Frames: {info['total_frames']}")

        success, frame = video.read_frame()

        if success:
            print("\nOriginal frame:")
            print(f"Shape: {frame.shape}")

            processed_frame = preprocessor.preprocess(frame)

            print("\nPreprocessed frame:")
            print(f"Shape: {processed_frame.shape}")
        else:
            print("\nCould not read the first frame.")

    finally:
        video.release()


if __name__ == "__main__":
    main()