from backend.database.mysql_service import get_connection


def save_alert(
    alert_type,
    severity,
    message,
    confidence=0.0,
    status="ACTIVE"
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO alerts (
                alert_type,
                severity,
                message,
                confidence,
                status
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                alert_type,
                severity,
                message,
                float(confidence),
                status
            )
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def get_recent_alerts(limit=20):
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                timestamp,
                alert_type,
                severity,
                message,
                confidence,
                status
            FROM alerts
            ORDER BY id DESC
            LIMIT %s
            """,
            (limit,)
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()