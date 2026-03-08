import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "admin",
    "password": "pass123",
    "port": 3306,
    "database": "gamecafe",
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_all_sessions():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT session_id, customer_id, station_id, start_time, end_time, total_cost FROM Session")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Error as e:
        return f"Error: {e}"

def create_active_session(customer_id, station_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Session (customer_id, station_id) VALUES (%s, %s)",
            (customer_id, station_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Error as e:
        return f"Error: {e}"
