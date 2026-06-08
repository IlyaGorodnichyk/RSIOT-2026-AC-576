# Лабораторная работа №4

<p align="center">Министерство образования Республики Беларусь</p>
<p align="center">Учреждение образования</p>
<p align="center">"Брестский Государственный технический университет"</p>
<p align="center">Кафедра ИИТ</p>
<br><br><br><br><br><br>
<p align="center"><strong>Лабораторная работа №4</strong></p>
<p align="center"><strong>По дисциплине:</strong> "Распределенные системы и облачные технологии"</p>
<p align="center"><strong>Тема:</strong> Наблюдаемость и метрики</p>
<br><br><br><br><br><br>
<p align="right"><strong>Выполнил:</strong></p>
<p align="right">Студент 4 курса</p>
<p align="right">Группы АС-576</p>
<p align="right">Городничук И. А.</p>
<p align="right"><strong>Проверил:</strong></p>
<p align="right">Несюк А. Н.</p>
<br><br><br><br><br>
<p align="center"><strong>Брест 2026</strong></p>

---

## Цель работы

Научиться устанавливать систему мониторинга в Kubernetes, добавить экспонирование метрик в приложение с использованием Prometheus client-библиотек.

---

### Вариант №02

**Параметры варианта:**

- Prefix метрик: `web02_`
- SLO: 99.6%
- p95 latency: 275ms
- Alert: "5xx > 1.5% за 10м"

## Метаданные студента

- **ФИО:** Городничук Илья Александрович
- **Группа:** АС-576
- **№ студенческого (StudentID):** 22023
- **Email (учебный):** [ваш email]
- **GitHub username:** [ваш username]
- **Вариант №:** 02
- **ОС и версия:** Windows 11, Docker Desktop v4.53.0

---

## Окружение и инструменты

- Kubernetes
- Helm
- Prometheus Operator (kube-prometheus-stack)
- Python 3.11
- Flask
- prometheus-client
- Docker (multi-stage)

## Структура репозитория
task_04/
├── app/
│ ├── app.py
│ └── requirements.txt
├── doc/
│ ├── README.md
│ ├── screenshots/
│ └── dashboards/
├── helm/web02/
│ ├── Chart.yaml
│ ├── values.yaml
│ └── templates/
│ ├── deployment.yaml
│ ├── service.yaml
│ ├── servicemonitor.yaml
│ └── prometheusrule.yaml
├── Dockerfile
└── k8s-deploy-fixed.yaml

## Подробное описание выполнения

### 1. Добавление метрик в приложение

Во Flask-приложение интегрирована библиотека prometheus-client.

Реализованы следующие метрики:

- `web02_http_requests_total` — Counter (счетчик запросов)
- `web02_http_request_latency_seconds` — Histogram (гистограмма задержек)
- `web02_service_up` — Gauge (статус сервиса)

**Эндпоинты приложения:**

- `/` — основной
- `/healthz` — проверка состояния
- `/error` — генерация ошибки 5xx
- `/metrics` — экспорт метрик

Метаданные студента логируются при запуске:
`STU_ID=22023`, `STU_GROUP=AS-576`, `STU_VARIANT=02`

### 2. Экспорт метрик

Метрики доступны по адресу:
/metrics
Формат — совместим с Prometheus. Префикс метрик — `web02_` (согласно варианту).

### 3. Docker-образ

Используется multi-stage Dockerfile:

- **Stage 1** — установка зависимостей
- **Stage 2** — минимальный runtime

Контейнер запускается от непривилегированного пользователя:
```dockerfile
USER 10001

dockerfile
LABEL org.bstu.student.fullname="Gorodnichuk Ilya Aleksandrovich"
LABEL org.bstu.student.id="22023"
LABEL org.bstu.group="AS-576"
LABEL org.bstu.variant="02"
LABEL org.bstu.course="RSIOT"

Создан Helm-чарт web02:

Chart.yaml — описание

values.yaml — параметры

templates/deployment.yaml — шаблон Deployment

templates/service.yaml — Service

templates/servicemonitor.yaml — сбор метрик

templates/prometheusrule.yaml — алерты

Развёртывание приложения
helm install web02 ./helm/web02 --namespace app-as576-v02 --create-namespace
# или через kubectl
kubectl apply -f k8s-deploy-fixed.yaml

Проверка:
kubectl get pods -n app-as576-v02
kubectl get svc -n app-as576-v02

Установка системы мониторинга

Установлен kube-prometheus-stack через Helm:
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring

ServiceMonitor
erviceMonitor подключает приложение к Prometheus:

Namespace: monitoring

Path: /metrics

Интервал сбора: 30s

Сбор метрик с сервиса web02-svc в namespace app-as576-v02

Alerting (PrometheusRule)

Реализованы два алерта согласно SLO:

1. High5xxErrorRate

Условие: 5xx ошибки > 1.5% за 10 минут

Severity: critical

For: 5m

2. HighLatencyP95

Условие: p95 latency > 275ms

Severity: warning

For: 5m

Дашборды Grafana
Созданы дашборды в Grafana:

Панель	Запрос PromQL	Порог SLO
Availability	sum(rate(web02_http_requests_total{status!~"5.."}[5m])) / sum(rate(web02_http_requests_total[5m])) * 100	99.6%
P95 Latency	histogram_quantile(0.95, sum(rate(web02_http_request_latency_seconds_bucket[5m])) by (le)) * 1000	275ms
Error Rate	sum(rate(web02_http_requests_total{status=~"5.."}[5m])) / sum(rate(web02_http_requests_total[5m])) * 100	1.5%

Доступ к сервисам
kubectl port-forward -n app-as576-v02 svc/web02-svc 9082:9082

# Prometheus
kubectl port-forward -n monitoring svc/prometheus-stack-kube-prom-prometheus 9090:9090

# Grafana
kubectl port-forward -n monitoring svc/prometheus-stack-grafana 3000:80
Приложение: http://localhost:9082

Prometheus: http://localhost:9090

Grafana: http://localhost:3000 (логин: admin)

Контрольный список (checklist)
[✅] Flask-приложение с метриками

[✅] Метрики Prometheus с префиксом web02_

[✅] Endpoint /metrics

[✅] Multi-stage Dockerfile

[✅] Non-root пользователь (USER 10001)

[✅] Helm Chart с параметризацией

[✅] Service для приложения

[✅] ServiceMonitor для сбора метрик

[✅] PrometheusRule (Alerting) по SLO

[✅] Логирование STU_ID / STU_GROUP / STU_VARIANT

[✅] Установка kube-prometheus-stack

[✅] Дашборды в Grafana

Вывод
В лабораторной работе реализована система наблюдаемости для Kubernetes-приложения.

Выполненные задачи:

Установлен и настроен стек мониторинга (kube-prometheus-stack: Prometheus + Grafana + Alertmanager)

В приложение интегрированы метрики с префиксом web02_ (согласно варианту)

Настроен ServiceMonitor для автоматического сбора метрик

Созданы дашборды в Grafana для визуализации ключевых метрик (доступность, задержка, ошибки)

Настроены алерты по SLO:

Доступность 99.6%

P95 latency < 275ms

Частота ошибок 5xx < 1.5% за 10 минут

Приложение упаковано в Helm-чарт с параметризацией

Приложение экспортирует метрики в формате Prometheus, настроен их сбор через ServiceMonitor, а также реализованы алерты для контроля ошибок и задержек. Использование Helm упростило деплой и конфигурацию приложения. Получены практические навыки мониторинга и анализа состояния сервисов в Kubernetes.

Результат: Система наблюдаемости полностью развернута и готова к мониторингу SLO приложения.



