# drf_4_project

REST API проект на Django Rest Framework с PostgreSQL и Docker.

## ⚠️ Порт
Порт **8000 занят**, проект работает на **8001**

## 🚀 Запуск

```bash
docker compose build
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
