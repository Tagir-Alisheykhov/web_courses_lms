# LMS веб-приложение

>Данная LMS-система разработана для того, чтобы каждый желающий мог размещать свои полезные материалы или курсы.

[![Django](https://img.shields.io/badge/Django-3.2.18-blue?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST](https://img.shields.io/badge/DRF-3.16.0-red?logo=json&logoColor=white)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

---

## 🧰 Установка

### 1. Клонируй репозиторий
```commandline
git clone git@github.com:Tagir-Alisheykhov/web_courses_lms.git
``` 
```commandline
cd WebCoursesLMS
```

### 2. Настройка виртуального окружения
```bash
python -m venv venv
```
```bash
source venv/bin/activate  # Linux/Mac
```
```bash
venv\Scripts\activate     # Windows
```
```bash
pip install -r requirements.txt
```

### 4. Миграции
-- Выполните миграцию в базу данных
```bash
python manage.py migrate
```

### 5. Запуск сервера
```bash
python manage.py runserver
```
-- После успешного запуска откройте: http://localhost:8000


### 📦 Возможные доработки проекта
- ✅ Интеграция Celery
- ✅ Графики статистики
- ✅ API (DRF)
- ✅ Поддержка i18n
- ✅ Email-уведомления

### 📄 Лицензия
- MIT License © 2025
