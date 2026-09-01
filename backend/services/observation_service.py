from backend.database.mysql_service import get_connection


def get_recent_observations(limit=20):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                timestamp,
                crowd_count,
                density,
                average_movement,
                dominant_direction,
                flow_consistency,
                risk_score,
                risk_level
            FROM crowd_observations
            ORDER BY id DESC
            LIMIT %s
            """,
            (limit,)
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()