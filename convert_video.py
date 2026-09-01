import os
import subprocess
import imageio_ffmpeg


INPUT_VIDEO = os.path.abspath(
    r"outputs\annotated_test.mp4"
)

OUTPUT_VIDEO = os.path.abspath(
    r"outputs\annotated_browser.mp4"
)


print("Input:")
print(INPUT_VIDEO)

print("\nOutput:")
print(OUTPUT_VIDEO)


if not os.path.exists(INPUT_VIDEO):

    print("\nERROR: Input video not found.")
    raise SystemExit(1)


ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

print("\nUsing FFmpeg:")
print(ffmpeg)

print("\nConverting video...")
print("This may take some time for a large video.\n")


command = [
    ffmpeg,

    "-y",

    "-i",
    INPUT_VIDEO,

    # H.264 video
    "-c:v",
    "libx264",

    # Browser-compatible pixel format
    "-pix_fmt",
    "yuv420p",

    # Good quality
    "-preset",
    "medium",

    "-crf",
    "23",

    # No audio needed for this CCTV demo
    "-an",

    # Put MP4 metadata at the beginning
    # so browser playback can start immediately
    "-movflags",
    "+faststart",

    OUTPUT_VIDEO
]


result = subprocess.run(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)


print(result.stdout)


if result.returncode != 0:

    print("\nERROR: FFmpeg conversion failed.")
    raise SystemExit(1)


if not os.path.exists(OUTPUT_VIDEO):

    print("\nERROR: Output video was not created.")
    raise SystemExit(1)


size_mb = (
    os.path.getsize(OUTPUT_VIDEO)
    / (1024 * 1024)
)


print("\n===================================")
print("CONVERSION SUCCESSFUL")
print("===================================")

print(
    f"Output size: {size_mb:.2f} MB"
)

print(
    f"Output file:\n{OUTPUT_VIDEO}"
)