from backend.database.mysql_service import (
    test_connection
)


if __name__ == "__main__":

    database = test_connection()

    print(
        f"MySQL connection successful!"
    )

    print(
        f"Database: {database}"
    )