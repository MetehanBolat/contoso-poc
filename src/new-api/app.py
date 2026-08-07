import os

from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Read App Service application settings
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SSLMODE = os.getenv("POSTGRES_SSLMODE", "require")

# Build PostgreSQL connection string
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
    f"/{POSTGRES_DB}"
    f"?sslmode={POSTGRES_SSLMODE}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

@app.route("/")
def home():
    return jsonify({
        "application": "Azure PostgreSQL Demo",
        "status": "running"
    })

@app.route("/dbtest")
def dbtest():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database();"))
            database_name = result.scalar()

        return jsonify({
            "success": True,
            "database": database_name
        })

    except Exception as ex:
        return jsonify({
            "success": False,
            "error": str(ex)
        }), 500

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


@app.route("/init")
def init_db():
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS app_log (
                    id SERIAL PRIMARY KEY,
                    message VARCHAR(200),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

            conn.execute(text("""
                INSERT INTO app_log (message)
                VALUES ('Application initialized')
            """))

        return jsonify({"success": True})

    except Exception as ex:
        return jsonify({
            "success": False,
            "error": str(ex)
        }), 500

@app.route("/logs")
def logs():
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT id, message, created_at
                FROM app_log
                ORDER BY id DESC
            """))

            data = [
                {
                    "id": row.id,
                    "message": row.message,
                    "created_at": str(row.created_at)
                }
                for row in rows
            ]

        return jsonify(data)

    except Exception as ex:
        return jsonify({
            "success": False,
            "error": str(ex)
        }), 500

