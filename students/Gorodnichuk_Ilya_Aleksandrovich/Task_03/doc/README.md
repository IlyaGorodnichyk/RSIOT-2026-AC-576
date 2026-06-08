# Лабораторная работа №03

<p align="center">Министерство образования Республики Беларусь</p>
<p align="center">Учреждение образования</p>
<p align="center">“Брестский Государственный технический университет”</p>
<p align="center">Кафедра ИИТ</p>
<br><br><br><br><br><br>
<p align="center"><strong>Лабораторная работа №03</strong></p>
<p align="center"><strong>По дисциплине:</strong> “Распределенные системы и облачные технологии”</p>
<p align="center"><strong>Тема:</strong> Kubernetes: состояние и хранение (StatefulSet, PVC/PV, Headless Service, backup/restore)</p>
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

Развернуть stateful-приложение Redis в Kubernetes: применить StatefulSet, настроить постоянное хранилище через PVC/PV, создать Headless Service для стабильных DNS-имён подов, добавить периодический backup (CronJob) и Job для восстановления данных, проверить сохранность данных при перезапуске пода.

---

### Вариант №02

## Метаданные студента

- **ФИО:** Городничук Илья Александрович
- **Группа:** АС-576
- **№ студенческого (StudentID):** 22023
- **Email (учебный):** <as576023@bstu.by>
- **GitHub username:** GorodnichukIlya
- **Вариант №:** 02
- **ОС и версия:** Windows 10, Docker Desktop v4.53.0, Kubernetes v1.34.3

---

## Структура файлов
task_03/src/k8s/
├── backup-cronjob.yaml – CronJob для резервного копирования Redis
├── backup-pvc.yaml – PVC для хранения резервных копий (5Gi)
├── headless-service.yaml – Headless Service для Redis
├── namespace.yaml – Namespace
├── restore-job.yaml – Job для восстановления данных
├── secret.yaml – Secret с паролем Redis
├── statefulset.yaml – StatefulSet Redis
└── storageclass.yaml – StorageClass


## Описание реализации

### 1. Namespace

Создан отдельный namespace:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: state-as-576-22023-v02
  labels:
    org.bstu.student.fullname: "Gorodnichuk.Ilya.Aleksandrovich"
    org.bstu.student.id: "22023"
    org.bstu.group: "AS-576"
    org.bstu.variant: "02"
    org.bstu.course: "RSIOT"

    Команды для запуска

    kubectl apply -f namespace.yaml
kubectl apply -f storageclass.yaml
kubectl apply -f secret.yaml
kubectl apply -f backup-pvc.yaml
kubectl apply -f headless-service.yaml
kubectl apply -f statefulset.yaml
kubectl apply -f backup-cronjob.yaml
kubectl apply -f restore-job.yaml

# Проверка статуса
kubectl get all,secret,pvc -n state-as-576-22023-v02

# Создание тестовых данных
kubectl exec -it -n state-as-576-22023-v02 db-redis-0 -- redis-cli -a redispass22023 --no-auth-warning SET user:1 "Gorodnichuk Ilya"
kubectl exec -it -n state-as-576-22023-v02 db-redis-0 -- redis-cli -a redispass22023 --no-auth-warning SET student:id "22023"

# Ручной запуск бэкапа
kubectl create job -n state-as-576-22023-v02 manual-backup --from=cronjob/backup-redis

# Просмотр логов бэкапа
kubectl logs -n state-as-576-22023-v02 job/manual-backup

# Восстановление данных
kubectl apply -f restore-job.yaml
kubectl logs -n state-as-576-22023-v02 job/restore-redis

Проверка сохранности данных после перезапуска пода:
bash
# Данные до перезапуска
$ kubectl exec -n state-as-576-22023-v02 db-redis-0 -- redis-cli -a redispass22023 --no-auth-warning GET user:1
"Gorodnichuk Ilya"

# Перезапуск пода
$ kubectl delete pod -n state-as-576-22023-v02 db-redis-0
pod "db-redis-0" deleted

# Данные после перезапуска
$ kubectl exec -n state-as-576-22023-v02 db-redis-0 -- redis-cli -a redispass22023 --no-auth-warning GET user:1
"Gorodnichuk Ilya"

Результат бэкапа:

Starting backup at Mon Jun 8 20:03:07 UTC 2026
Background saving started
OK
Backup completed: /backup/redis-dump-20260608-200312.rdb
total 8K
-rw-r--r-- 1 root root 234 Jun 8 20:02 redis-dump-20260608-200250.rdb
-rw-r--r-- 1 root root 234 Jun 8 20:03 redis-dump-20260608-200312.rdb

Результат восстановления:
Available backups:
redis-dump-20260608-200250.rdb
redis-dump-20260608-200312.rdb
Restoring from: /backup/redis-dump-20260608-200312.rdb
Restore completed successfully!

Контрольный список
[✅] Namespace создан с метаданными

[✅] Secret с паролем Redis

[✅] StorageClass (rancher.io/local-path)

[✅] PVC для данных (5Gi) и для бэкапов (5Gi)

[✅] StatefulSet с volumeClaimTemplates

[✅] Headless Service (clusterIP: None)

[✅] CronJob для бэкапов (каждый час)

[✅] Job для восстановления

[✅] Сохранение данных после перезапуска пода

[✅] Успешное восстановление из бэкапа

Вывод
В ходе лабораторной работы было развернуто stateful-приложение Redis в Kubernetes с использованием:

StatefulSet для управления stateful-приложением

PersistentVolumeClaim (5Gi) для постоянного хранения данных

Headless Service для стабильных DNS-имён

CronJob для автоматического резервного копирования (каждый час)

Job для восстановления данных из резервной копии

Данные Redis сохраняются при перезапуске пода, что подтверждает корректность использования StatefulSet и PVC. Механизм резервного копирования и восстановления работает успешно, что позволяет восстанавливать данные после их удаления.