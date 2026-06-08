FROM python:3.11-slim AS builder

WORKDIR /build
COPY app/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

LABEL org.bstu.student.fullname="Gorodnichuk_Ilya_Aleksandrovich"
LABEL org.bstu.student.id="22023"
LABEL org.bstu.group="AS-576"
LABEL org.bstu.variant="w2"
LABEL org.bstu.course="RSIOT"

ENV STU_ID=22023 \
    STU_GROUP=AS-576 \
    STU_VARIANT=w2 \
    DB_HOST=postgres \
    DB_PORT=5432 \
    POSTGRES_DB=app_22023_vw2 \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=postgres123 \
    PYTHONUNBUFFERED=1

RUN addgroup --gid 10001 appgroup && \
    adduser --uid 10001 --gid 10001 --disabled-password --no-create-home appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local

COPY app/app.py .

ENV PATH=/home/appuser/.local/bin:$PATH

RUN chown -R appuser:appgroup /app && \
    chmod 755 /app/app.py

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9082/healthz')" || exit 1

EXPOSE 9082

CMD ["python", "app.py"]