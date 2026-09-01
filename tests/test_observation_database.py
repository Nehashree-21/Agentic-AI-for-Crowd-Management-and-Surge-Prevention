from backend.database.observation_service import (
    save_crowd_observation
)

from backend.database.mysql_service import (
    get_connection
)


save_crowd_observation(
    crowd_count=29,
    density="MEDIUM",
    average_movement=6.9,
    dominant_direction="UP",
    flow_consistency=88.89,
    risk_score=75,
    risk_level="CRITICAL"
)

print("Observation saved successfully!")


connection = get_connection()

try:
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            crowd_count,
            density,
            risk_score,
            risk_level
        FROM crowd_observations
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    print("\nLatest observation:")
    print(row)

finally:
    cursor.close()
    connection.close()