from sqlalchemy import create_engine, text
from datetime import datetime
import pandas as pd

# ---------------- DATABASE CONNECTION ---------------- #

DB_URL = "postgresql://postgres:root1234@localhost:5432/sentinelpulse_db"

engine = create_engine(DB_URL)

# ---------------- CREATE TABLE ---------------- #

def create_tables():

    query = """

    CREATE TABLE IF NOT EXISTS machine_diagnostics (

        id SERIAL PRIMARY KEY,

        temperature FLOAT,
        vibration FLOAT,
        pressure FLOAT,

        risk_score INTEGER,
        status VARCHAR(50),

        created_at TIMESTAMP

    );

    """

    with engine.connect() as conn:

        conn.execute(text(query))
        conn.commit()

# ---------------- SAVE PREDICTION ---------------- #

def save_prediction(
    temperature,
    vibration,
    pressure,
    risk_score,
    status
):

    query = text("""

        INSERT INTO machine_diagnostics (

            temperature,
            vibration,
            pressure,
            risk_score,
            status,
            created_at

        )

        VALUES (

            :temperature,
            :vibration,
            :pressure,
            :risk_score,
            :status,
            :created_at

        )

    """)

    with engine.connect() as conn:

        conn.execute(
            query,
            {
                "temperature": temperature,
                "vibration": vibration,
                "pressure": pressure,
                "risk_score": risk_score,
                "status": status,
                "created_at": datetime.now()
            }
        )

        conn.commit()

# ---------------- FETCH PREDICTIONS ---------------- #

def fetch_predictions():

    query = """

    SELECT * FROM machine_diagnostics
    ORDER BY id DESC;

    """

    df = pd.read_sql(query, engine)

    return df

    # ---------------- CREATE SYSTEM LOG TABLE ---------------- #

def create_system_logs_table():

    query = """

    CREATE TABLE IF NOT EXISTS system_logs (

        id SERIAL PRIMARY KEY,

        event_type VARCHAR(100),

        event_message TEXT,

        created_at TIMESTAMP

    );

    """

    with engine.connect() as conn:

        conn.execute(text(query))
        conn.commit()

# ---------------- SAVE SYSTEM EVENT ---------------- #

def save_system_log(
    event_type,
    event_message
):

    query = text("""

        INSERT INTO system_logs (

            event_type,
            event_message,
            created_at

        )

        VALUES (

            :event_type,
            :event_message,
            :created_at

        )

    """)

    with engine.connect() as conn:

        conn.execute(
            query,
            {
                "event_type": event_type,
                "event_message": event_message,
                "created_at": datetime.now()
            }
        )

        conn.commit()

# ---------------- FETCH SYSTEM LOGS ---------------- #

def fetch_system_logs():

    query = """

    SELECT *
    FROM system_logs
    ORDER BY id DESC;

    """

    df = pd.read_sql(query, engine)

    return df