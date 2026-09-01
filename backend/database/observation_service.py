from backend.database.mysql_service import get_connection


def save_crowd_observation(
    crowd_count,
    density,
    average_movement,
    dominant_direction,
    flow_consistency,
    risk_score,
    risk_level
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO crowd_observations (
                crowd_count,
                density,
                average_movement,
                dominant_direction,
                flow_consistency,
                risk_score,
                risk_level
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            int(crowd_count),
            str(density),
            float(average_movement),
            str(dominant_direction),
            float(flow_consistency),
            int(risk_score),
            str(risk_level)
        )

        cursor.execute(query, values)
        connection.commit()

    finally:
        cursor.close()
        connection.close()