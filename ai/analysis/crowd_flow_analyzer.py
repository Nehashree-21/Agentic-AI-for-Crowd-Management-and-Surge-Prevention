from collections import Counter


class CrowdFlowAnalyzer:

    def __init__(self):
        self.previous_average = None

    def analyze(self, movements):
        """
        Analyze movement of all tracked people
        in the current frame.
        """

        if not movements:
            return {
                "total_tracked": 0,
                "direction_distribution": {},
                "dominant_direction": "UNKNOWN",
                "flow_consistency": 0.0,
                "average_displacement": 0.0,
                "movement_change": 0.0
            }

        directions = [
            movement["direction"]
            for movement in movements
        ]

        direction_counts = Counter(directions)

        total = len(directions)

        direction_distribution = {
            direction: round(
                count / total * 100,
                2
            )
            for direction, count
            in direction_counts.items()
        }

        # Ignore stationary people when determining
        # the dominant moving direction.
        moving_directions = [
            direction
            for direction in directions
            if direction != "STATIONARY"
        ]

        if moving_directions:

            moving_counts = Counter(
                moving_directions
            )

            dominant_direction = (
                moving_counts.most_common(1)[0][0]
            )

            dominant_count = (
                moving_counts[
                    dominant_direction
                ]
            )

            flow_consistency = round(
                dominant_count
                / len(moving_directions)
                * 100,
                2
            )

        else:

            dominant_direction = "STATIONARY"
            flow_consistency = 100.0

        average_displacement = round(
            sum(
                movement["displacement"]
                for movement in movements
            ) / total,
            2
        )

        # Compare current movement with
        # previous observation.
        if self.previous_average is None:

            movement_change = 0.0

        elif self.previous_average == 0:

            movement_change = 0.0

        else:

            movement_change = round(
                (
                    (
                        average_displacement
                        - self.previous_average
                    )
                    / self.previous_average
                ) * 100,
                2
            )

        self.previous_average = (
            average_displacement
        )

        return {
            "total_tracked": total,
            "direction_distribution":
                direction_distribution,
            "dominant_direction":
                dominant_direction,
            "flow_consistency":
                flow_consistency,
            "average_displacement":
                average_displacement,
            "movement_change":
                movement_change
        }
    