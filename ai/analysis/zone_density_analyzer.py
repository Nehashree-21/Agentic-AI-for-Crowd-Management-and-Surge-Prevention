class ZoneDensityAnalyzer:

    def __init__(
        self,
        frame_width,
        frame_height,
        rows=3,
        cols=3
    ):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.rows = rows
        self.cols = cols

        self.zone_width = (
            frame_width / cols
        )

        self.zone_height = (
            frame_height / rows
        )

    def get_zone_id(self, center_x, center_y):

        col = int(
            center_x / self.zone_width
        )

        row = int(
            center_y / self.zone_height
        )

        # Prevent boundary errors
        col = min(
            max(col, 0),
            self.cols - 1
        )

        row = min(
            max(row, 0),
            self.rows - 1
        )

        return (
            row * self.cols
        ) + col + 1

    def analyze(self, people):

        zone_counts = {
            zone: 0
            for zone in range(
                1,
                self.rows * self.cols + 1
            )
        }

        for person in people:

            x1, y1, x2, y2 = (
                person["bbox"]
            )

            center_x = (
                x1 + x2
            ) / 2

            center_y = (
                y1 + y2
            ) / 2

            zone_id = self.get_zone_id(
                center_x,
                center_y
            )

            zone_counts[
                zone_id
            ] += 1

        total_people = len(
            people
        )

        zone_results = {}

        for zone, count in (
            zone_counts.items()
        ):

            if total_people > 0:

                percentage = (
                    count
                    / total_people
                    * 100
                )

            else:

                percentage = 0

            density_level = (
                self._get_density_level(
                    count
                )
            )

            zone_results[zone] = {
                "count": count,
                "percentage": round(
                    percentage,
                    2
                ),
                "density": density_level
            }

        return zone_results

    def _get_density_level(
        self,
        count
    ):

        if count >= 15:
            return "VERY HIGH"

        if count >= 10:
            return "HIGH"

        if count >= 5:
            return "MEDIUM"

        if count >= 1:
            return "LOW"

        return "EMPTY"

    def get_overall_density(
        self,
        zone_results
    ):

        levels = [
            result["density"]
            for result
            in zone_results.values()
        ]

        if "VERY HIGH" in levels:
            return "VERY HIGH"

        if levels.count("HIGH") >= 2:
            return "HIGH"

        if "HIGH" in levels:
            return "HIGH"

        if levels.count("MEDIUM") >= 2:
            return "MEDIUM"

        if "MEDIUM" in levels:
            return "MEDIUM"

        if "LOW" in levels:
            return "LOW"

        return "EMPTY"