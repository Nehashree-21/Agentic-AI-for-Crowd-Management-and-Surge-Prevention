from collections import defaultdict
import math


class MovementAnalyzer:
    def __init__(self):
        self.previous_positions = {}
        self.track_history = defaultdict(list)

    def update(self, people):
        movements = []

        for person in people:
            track_id = person["track_id"]

            x1, y1, x2, y2 = person["bbox"]

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            current_position = (center_x, center_y)

            previous_position = self.previous_positions.get(
                track_id
            )

            if previous_position is None:
                dx = 0
                dy = 0
                distance = 0
                direction = "STATIONARY"
            else:
                dx = center_x - previous_position[0]
                dy = center_y - previous_position[1]

                distance = math.sqrt(
                    dx ** 2 + dy ** 2
                )

                direction = self._get_direction(
                    dx,
                    dy
                )

            self.previous_positions[
                track_id
            ] = current_position

            self.track_history[
                track_id
            ].append(current_position)

            movements.append({
                "track_id": track_id,
                "center": (
                    round(center_x, 2),
                    round(center_y, 2)
                ),
                "dx": round(dx, 2),
                "dy": round(dy, 2),
                "displacement": round(
                    distance,
                    2
                ),
                "direction": direction
            })

        return movements

    def _get_direction(self, dx, dy):

        threshold = 3

        if abs(dx) < threshold and abs(dy) < threshold:
            return "STATIONARY"

        if abs(dx) > abs(dy):

            if dx > 0:
                return "RIGHT"

            return "LEFT"

        if dy > 0:
            return "DOWN"

        return "UP"

    def get_average_speed(self, movements):

        if not movements:
            return 0

        total = sum(
            movement["displacement"]
            for movement in movements
        )

        return round(
            total / len(movements),
            2
        )