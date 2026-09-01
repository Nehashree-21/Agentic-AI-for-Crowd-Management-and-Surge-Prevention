import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def test_connection():

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")

        result = cursor.fetchone()

        return result[0]

    finally:
        cursor.close()
        connection.close()