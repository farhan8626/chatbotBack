import mysql.connector
from mysql.connector import Error
import json
import os

# Configuration for MySQL connection
# Can be overridden by environment variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Farhan@8626")
DB_NAME = os.environ.get("DB_NAME", "quantan_db")

def execute_query(query: str, params: tuple = None) -> str:
    """
    Executes a MySQL query safely using parameterized inputs.
    Returns the results as a JSON string.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            # If it's a SELECT query, fetch results
            if query.strip().upper().startswith("SELECT"):
                records = cursor.fetchall()
                # Handle datetime/decimal serialization if needed
                return json.dumps(records, default=str)
            else:
                connection.commit()
                return json.dumps({"status": "success", "rows_affected": cursor.rowcount})

    except Error as e:
        return json.dumps({"error": str(e), "status": "failed"})
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
