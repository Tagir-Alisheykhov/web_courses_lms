# LMS веб-приложение

>Данная LMS-система разработана для того, чтобы каждый желающий мог размещать свои полезные материалы или курсы.

[![Django](https://img.shields.io/badge/Django-3.2.18-blue?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST](https://img.shields.io/badge/DRF-3.16.0-red?logo=json&logoColor=white)](https://www.django-rest-framework.org/)
[![Django Filter](https://img.shields.io/badge/django--filter-23.1-blue?logo=filter&logoColor=white)](https://django-filter.readthedocs.io/en/stable/)
[![SimpleJWT](https://img.shields.io/badge/Simple_JWT-5.2.2-ff69b4?logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python&logoColor=white)](https://www.python.org/)
[![drf-yasg](https://img.shields.io/badge/drf--yasg-1.21.6-brightgreen?logo=swagger&logoColor=white)](https://drf-yasg.readthedocs.io/en/stable/readme.html#usage)
[![django-cors-headers](https://img.shields.io/badge/django--cors--headers-4.3.1-success?logo=cors&logoColor=white)](https://pypi.org/project/django-cors-headers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

---

## 🧰 Установка и настройка проекта

### 1. Клонируйте репозиторий
```commandline
git clone git@github.com:Tagir-Alisheykhov/web_courses_lms.git
``` 
```commandline
cd WebCoursesLMS   
```

### 2. Настройка виртуального окружения
>Для начала убедитесь, что на вашем ПК установлен `poetry`
```bash
poetry install    # Установка зависимостей в виртуальное окружение
```
```bash
poetry shell    # Активация виртуального окружения 
```


### 3. Миграции
>Выполните миграцию в базу данных
```bash
python manage.py migrate
```

### 4. Наполнение базы данных
> После успешной миграции, вы можете наполнить базу данных тестовыми данными (для моделей: User; Payment;
> Course; Lesson, а также для класса Group). Для этого выполните следующую команду:
```bash
python manage.py create_mock_data
```


### 5. Запуск сервера
```bash
python manage.py runserver
```
>После успешного запуска откройте: http://localhost:8000

---

## 📄 Лицензия
- MIT License © 2025
