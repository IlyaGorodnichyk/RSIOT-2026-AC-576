import os
import signal
import sys
import time
import logging
from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

STU_ID = os.getenv("STU_ID", "unknown")
STU_GROUP = os.getenv("STU_GROUP", "unknown")
STU_VARIANT = os.getenv("STU_VARIANT", "w2")

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", f"app_{STU_ID}_v{STU_VARIANT}")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres123")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def handle_sigterm(signum, frame):
    logger.info("SIGTERM received. Graceful shutdown started...")
    time.sleep(2)
    logger.info("Application stopped gracefully")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=5
        )
        return conn
    except Exception as e:
        logger.error(f"DB connection error: {e}")
        return None

def init_database():
    conn = get_db_connection()
    if not conn:
        logger.error("Failed to initialize database")
        return
    
    try:
        cur = conn.cursor()
        table_name = f"visits_{STU_VARIANT}"
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                student_id VARCHAR(50) NOT NULL UNIQUE,
                visit_count INTEGER DEFAULT 0,
                last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        logger.info(f"Table {table_name} created/verified")
    except Exception as e:
        logger.error(f"Init error: {e}")
    finally:
        conn.close()


@app.route("/")
def index():
    logger.info(f"Home page - student {STU_ID}")
    return jsonify({
        "message": "Flask app is running",
        "student_id": STU_ID,
        "group": STU_GROUP,
        "variant": STU_VARIANT,
        "port": 9082,
        "database": DB_NAME
    })

@app.route("/healthz")
def health():
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return jsonify({"status": "ok"}), 200
        return jsonify({"status": "fail", "error": "DB not connected"}), 503
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500

@app.route("/visit")
def visit():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 503
    
    try:
        cur = conn.cursor()
        table_name = f"visits_{STU_VARIANT}"
        
        cur.execute(f"""
            INSERT INTO {table_name} (student_id, visit_count)
            VALUES (%s, 1)
            ON CONFLICT (student_id) 
            DO UPDATE SET visit_count = {table_name}.visit_count + 1,
                          last_visit = CURRENT_TIMESTAMP
            RETURNING visit_count
        """, (STU_ID,))
        
        visits = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        logger.info(f"Visit #{visits} from student {STU_ID}")
        
        return jsonify({
            "student_id": STU_ID,
            "variant": STU_VARIANT,
            "visits": visits,
            "message": f"Hello from variant {STU_VARIANT}"
        })
    except Exception as e:
        logger.error(f"Counter error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/stats")
def stats():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "DB connection failed"}), 503
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        table_name = f"visits_{STU_VARIANT}"
        cur.execute(f"""
            SELECT student_id, visit_count, last_visit
            FROM {table_name}
            WHERE student_id = %s
        """, (STU_ID,))
        result = cur.fetchone()
        cur.close()
        
        if result:
            return jsonify(dict(result))
        return jsonify({"student_id": STU_ID, "visit_count": 0})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info(f"STARTING APPLICATION (VARIANT {STU_VARIANT})")
    logger.info(f"Student: {STU_ID}")
    logger.info(f"Group: {STU_GROUP}")
    logger.info(f"Port: 9082")
    logger.info(f"Health: /healthz")
    logger.info(f"Database: {DB_NAME}")
    logger.info("=" * 50)
    
    init_database()
    app.run(host="0.0.0.0", port=9082, debug=False)