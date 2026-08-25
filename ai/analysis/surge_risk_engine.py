class SurgeRiskEngine:

    def __init__(
        self,
        baseline_movement=3.04,
        baseline_movement_std=1.50,
        baseline_density=2.18,
        baseline_density_std=0.40
    ):
        self.baseline_movement = baseline_movement
        self.baseline_movement_std = baseline_movement_std

        self.baseline_density = baseline_density
        self.baseline_density_std = baseline_density_std

    def calculate_z_score(self, value, mean, std):

        if std <= 0:
            return 0.0

        return (
            value - mean
        ) / std

    def calculate_score(
        self,
        average_displacement,
        density_level,
        flow_consistency,
        movement_change
    ):

        # --------------------------------
        # 1. Movement anomaly: 0–30
        # --------------------------------

        movement_z = self.calculate_z_score(
            average_displacement,
            self.baseline_movement,
            self.baseline_movement_std
        )

        if movement_z >= 2.5:
            movement_score = 30

        elif movement_z >= 2.0:
            movement_score = 25

        elif movement_z >= 1.5:
            movement_score = 20

        elif movement_z >= 1.0:
            movement_score = 12

        elif movement_z >= 0.5:
            movement_score = 6

        else:
            movement_score = 0

        # --------------------------------
        # 2. Density score: 0–25
        # --------------------------------

        density_number = {
            "EMPTY": 0,
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "VERY HIGH": 4
        }.get(
            density_level,
            0
        )

        density_z = self.calculate_z_score(
            density_number,
            self.baseline_density,
            self.baseline_density_std
        )

        if density_z >= 2:
            density_score = 25

        elif density_z >= 1:
            density_score = 18

        elif density_z >= 0.5:
            density_score = 10

        else:
            density_score = 0

        # --------------------------------
        # 3. Flow consistency: 0–20
        # --------------------------------

        if flow_consistency >= 85:
            flow_score = 20

        elif flow_consistency >= 70:
            flow_score = 15

        elif flow_consistency >= 55:
            flow_score = 10

        elif flow_consistency >= 40:
            flow_score = 5

        else:
            flow_score = 0

        # --------------------------------
        # 4. Movement change: 0–25
        # --------------------------------

        if movement_change >= 100:
            acceleration_score = 25

        elif movement_change >= 60:
            acceleration_score = 20

        elif movement_change >= 40:
            acceleration_score = 15

        elif movement_change >= 20:
            acceleration_score = 10

        elif movement_change >= 10:
            acceleration_score = 5

        else:
            acceleration_score = 0

        # --------------------------------
        # Total
        # --------------------------------

        total_score = (
            movement_score
            + density_score
            + flow_score
            + acceleration_score
        )

        # --------------------------------
        # Risk classification
        # --------------------------------

        if total_score >= 70:
            risk_level = "CRITICAL"

        elif total_score >= 40:
            risk_level = "WARNING"

        else:
            risk_level = "LOW"

        return {
            "risk_score": total_score,
            "risk_level": risk_level,

            "movement_z_score": round(
                movement_z,
                2
            ),

            "density_z_score": round(
                density_z,
                2
            ),

            "movement_score": movement_score,
            "density_score": density_score,
            "flow_score": flow_score,
            "acceleration_score":
                acceleration_score
        }