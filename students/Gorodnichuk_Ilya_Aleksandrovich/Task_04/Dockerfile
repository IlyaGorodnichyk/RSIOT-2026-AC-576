FROM python:3.12-slim AS builder
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

# Исправлено: ваши данные
LABEL org.bstu.student.fullname="Gorodnichuk Ilya Aleksandrovich" \
      org.bstu.student.id="22023" \
      org.bstu.group="AS-576" \
      org.bstu.variant="02" \
      org.bstu.course="RSIOT"

RUN useradd -u 10001 appuser
WORKDIR /app

COPY --from=builder /install /usr/local
COPY app /app

USER 10001
EXPOSE 8082

CMD ["python", "app.py"]