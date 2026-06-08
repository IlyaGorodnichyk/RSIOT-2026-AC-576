import os
import time
import signal
import sys
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Префикс по вашему варианту
PREFIX = "web02_"

# Метрики Prometheus
REQUESTS = Counter(f"{PREFIX}http_requests_total", "Total HTTP requests", ["method", "path", "status"])
LATENCY = Histogram(f"{PREFIX}http_request_latency_seconds", "Request latency", ["path"])
STATUS = Gauge(f"{PREFIX}service_up", "Service status")

# Переменные окружения
STU_ID = os.getenv("STU_ID", "22023")
STU_GROUP = os.getenv("STU_GROUP", "AS-576")
STU_VARIANT = os.getenv("STU_VARIANT", "02")

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
    STATUS.set(1)
    return jsonify({
        "student_id": STU_ID,
        "group": STU_GROUP,
        "variant": STU_VARIANT,
        "database": f"app_{STU_ID}_v{STU_VARIANT}",
        "message": "Flask app is running",
        "port": 9082
    })

@app.route("/healthz")
def health():
    STATUS.set(1)
    return jsonify({"status": "ok", "service": "healthy"})

@app.route("/error")
def error():
    """Эндпоинт для генерации ошибок 5xx"""
    return jsonify({"error": "Simulated error"}), 500

@app.route("/metrics")
def metrics():
    """Эндпоинт для Prometheus"""
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    print(f"Starting app with STU_ID={STU_ID}, GROUP={STU_GROUP}, VARIANT={STU_VARIANT}")
    print(f"Metrics available at /metrics with prefix {PREFIX}")
    app.run(host="0.0.0.0", port=9082)
