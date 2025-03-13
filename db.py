# db.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_conn():
    """
    Returns a connection to the forecast_app_db.
    Expects DATABASE_URL or default to local connection.
    e.g. postgresql://forecast_user:secretpassword@localhost:5432/forecast_app_db
    """
    database_url = os.getenv("DATABASE_URL", "postgresql://forecast_user:secretpassword@localhost:5432/forecast_app_db")
    conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
    return conn


def insert_dengue_data(date_observed, region, cases):
    conn = get_db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO dengue_data (date_observed, region, cases)
                VALUES (%s, %s, %s)
                """,
                (date_observed, region, cases)
            )
    conn.close()

def get_all_dengue():
    conn = get_db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM dengue_data ORDER BY date_observed")
            rows = cur.fetchall()
    conn.close()
    return rows
def insert_malaria_data(date_observed, region, cases):
    conn = get_db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO malaria_data (date_observed, region, cases)
                VALUES (%s, %s, %s)
                """,
                (date_observed, region, cases)
            )
    conn.close()

def get_all_malaria():
    conn = get_db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM malaria_data ORDER BY date_observed")
            rows = cur.fetchall()
    conn.close()
    return rows
