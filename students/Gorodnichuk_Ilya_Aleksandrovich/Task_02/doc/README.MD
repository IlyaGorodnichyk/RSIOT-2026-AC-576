# Лабораторная работа №02

<p align="center">Министерство образования Республики Беларусь</p>
<p align="center">Учреждение образования</p>
<p align="center">"Брестский Государственный технический университет"</p>
<p align="center">Кафедра ИИТ</p>
<br><br><br><br><br><br>
<p align="center"><strong>Лабораторная работа №02</strong></p>
<p align="center"><strong>По дисциплине:</strong> "Распределенные системы и облачные технологии"</p>
<p align="center"><strong>Тема:</strong> Kubernetes: базовый деплой</p>
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

Научиться готовить Kubernetes-манифесты для простого HTTP-сервиса.

---

### Вариант №02

## Метаданные студента

- **ФИО:** Городничук Илья Александрович
- **Группа:** АС-576
- **№ студенческого (StudentID):** 22023
- **Email (учебный):** [as576@bsty.email]
- **GitHub username:** [IlyaGorodnichyk]
- **Вариант №:** 2
- **ОС и версия:** Windows 11, Docker Desktop v4.53.0, kubectl v1.30.0, Docker Desktop Kubernetes

---

## Окружение и инструменты

- Python 3.12
- Flask 3.0.0
- Docker
- Kubernetes (Docker Desktop Kubernetes)

## Параметры деплоя

- **Namespace:** web02
- **Name:** app02
- **Replicas:** 3
- **Port:** 8082
- **CPU:** 200m
- **Memory:** 192Mi

## Структура репозитория

```text
Task_02/
├── doc/
│   └── readme.md           # Документация
├── src/
│   ├── app.py              # HTTP-сервер
│   ├── Dockerfile          # Сборка образа
│   ├── requirements.txt    # Зависимости Python
│   └── k8s/
│       ├── deployment-app/
│       │   ├── deployment.yaml
│       │   └── service.yaml
│       ├── configmap/
│       │   └── configmap.yaml
│       ├── secret/
│       │   └── secret.yaml
│       └── namespace/
│           └── namespace.yaml