import hashlib
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
import psycopg2
from psycopg2.extras import RealDictCursor
import os

################################
# 1. Digital Watermark
################################
WATERMARK = "Developed by Dr. Kaushik Sarkar, Director-IMACS | Forecast App 2025"
WATERMARK_HASH = hashlib.sha256(WATERMARK.encode()).hexdigest()

def verify_watermark():
    if hashlib.sha256(WATERMARK.encode()).hexdigest() != WATERMARK_HASH:
        print("Unauthorized modification detected! Exiting...")
        sys.exit(1)

verify_watermark()

################################
# 2. Database Setup
################################

def get_db_conn():
    """
    Creates a connection to the local PostgreSQL database.
    Provide a DATABASE_URL env variable OR fallback to local credentials.
    e.g. 'postgresql://forecast_user:secretpassword@localhost:5432/forecast_app_db'
    """
    database_url = os.getenv("DATABASE_URL", "postgresql://forecast_user:secretpassword@localhost:5432/forecast_app_db")
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

# Example: separate disease tables
# dengue_data, malaria_data, etc.

def insert_dengue_data(date_observed, region, cases):
    conn = get_db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO dengue_data (date_observed, region, cases)
                VALUES (%s, %s, %s)
            """, (date_observed, region, cases))
    conn.close()

def get_all_dengue():
    conn = get_db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM dengue_data ORDER BY date_observed")
            rows = cur.fetchall()
    conn.close()
    return rows

################################
# 3. FastAPI Application
################################
app = FastAPI(title="Forecast App with Watermark")

# Pydantic model for request body
class DiseaseRecord(BaseModel):
    date_observed: date
    region: str
    cases: int

@app.get("/")
def home():
    return {"message": "Welcome to the Forecast App API, Watermark enforced."}

# Example routes for dengue
@app.post("/dengue")
def add_dengue_record(record: DiseaseRecord):
    try:
        insert_dengue_data(record.date_observed, record.region, record.cases)
        return {"status": "dengue record inserted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dengue")
def list_dengue_records():
    try:
        records = get_all_dengue()
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

################################
# 4. Run (development mode)
################################
# If you want to run this with 'python app.py', do:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

