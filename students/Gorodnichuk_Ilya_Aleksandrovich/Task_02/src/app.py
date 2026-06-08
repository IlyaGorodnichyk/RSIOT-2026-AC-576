import os
import signal
import sys
import time
from flask import Flask, jsonify

app = Flask(__name__)

STU_ID = os.getenv("STU_ID")
STU_GROUP = os.getenv("STU_GROUP")
STU_VARIANT = os.getenv("STU_VARIANT")

running = True

def handle_sigterm(signum, frame):
    global running
    print("[INFO] SIGTERM received. Graceful shutdown started...")
    running = False
    time.sleep(2)
    print("[INFO] Application stopped gracefully.")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

@app.route("/")
def index():
    return jsonify(
        message="Kubernetes Flask App",
        student_id=STU_ID,
        group=STU_GROUP,
        variant=STU_VARIANT
    )

@app.route("/healthz")
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    print(f"[START] STU_ID={STU_ID}, GROUP={STU_GROUP}, VARIANT={STU_VARIANT}")
    print(f"[INFO] Starting Flask app on port 8082")
    app.run(host="0.0.0.0", port=8082)