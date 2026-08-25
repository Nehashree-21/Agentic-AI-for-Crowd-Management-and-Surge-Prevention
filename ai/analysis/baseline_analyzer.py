import statistics


class BaselineAnalyzer:

    def __init__(self):
        self.samples = []

    def add_sample(
        self,
        tracked_count,
        average_displacement,
        overall_density
    ):
        self.samples.append({
            "tracked_count": tracked_count,
            "average_displacement": average_displacement,
            "overall_density": overall_density
        })

    def calculate(self):

        if not self.samples:
            return {}

        counts = [
            sample["tracked_count"]
            for sample in self.samples
        ]

        movements = [
            sample["average_displacement"]
            for sample in self.samples
        ]

        density_values = [
            self._density_to_number(
                sample["overall_density"]
            )
            for sample in self.samples
        ]

        return {
            "sample_count": len(self.samples),

            "tracked_count": {
                "mean": round(
                    statistics.mean(counts),
                    2
                ),
                "std": round(
                    statistics.stdev(counts)
                    if len(counts) > 1 else 0,
                    2
                ),
                "minimum": min(counts),
                "maximum": max(counts)
            },

            "movement": {
                "mean": round(
                    statistics.mean(movements),
                    2
                ),
                "std": round(
                    statistics.stdev(movements)
                    if len(movements) > 1 else 0,
                    2
                ),
                "minimum": round(
                    min(movements),
                    2
                ),
                "maximum": round(
                    max(movements),
                    2
                )
            },

            "density": {
                "mean": round(
                    statistics.mean(density_values),
                    2
                ),
                "std": round(
                    statistics.stdev(density_values)
                    if len(density_values) > 1 else 0,
                    2
                )
            }
        }

    def _density_to_number(self, density):

        mapping = {
            "EMPTY": 0,
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "VERY HIGH": 4
        }

        return mapping.get(
            density,
            0
        )