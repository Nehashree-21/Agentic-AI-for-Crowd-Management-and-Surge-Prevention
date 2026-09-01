from ai.integration.crowd_monitor import (
    CrowdMonitor
)


VIDEO_PATH = "videos/test.mp4"


def main():

    monitor = CrowdMonitor(
        VIDEO_PATH
    )

    monitor.run()


if __name__ == "__main__":
    main()