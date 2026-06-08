import os
import time
import signal
import sys
from flask import Flask, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Исправлено: префикс по варианту
PREFIX = "web02_"

REQUESTS = Counter(f"{PREFIX}http_requests_total", "Total HTTP requests", ["method", "path", "status"])
LATENCY = Histogram(f"{PREFIX}http_request_latency_seconds", "Request latency", ["path"])
STATUS = Gauge(f"{PREFIX}service_up", "Service status")

STU_ID = os.getenv("STU_ID")
STU_GROUP = os.getenv("STU_GROUP")
STU_VARIANT = os.getenv("STU_VARIANT")

def shutdown(sig, frame):
    print("Graceful shutdown")
    STATUS.set(0)
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)

@app.before_request
def before():
    request.start_time = time.time()

@app.after_request
def after(response):
    latency = time.time() - request.start_time
    LATENCY.labels(request.path).observe(latency)
    REQUESTS.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route("/")
def index():
    return {"status": "ok"}

@app.route("/healthz")
def health():
    STATUS.set(1)
    return {"health": "ok"}

@app.route("/error")
def error():
    return {"error": "fail"}, 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    print(f"STU_ID={STU_ID}, GROUP={STU_GROUP}, VARIANT={STU_VARIANT}")
    app.run(host="0.0.0.0", port=8082)