"""
Celery задачи
"""

import os
from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from dotenv import load_dotenv

from users.models import User

load_dotenv()

sender = os.getenv("EMAIL_HOST_USER")
main_page = os.getenv("MAIN_PAGE")


@shared_task
def last_user_login():
    """
    Проверка последнего входа всех пользователей.
    Деактивация неактивных пользователей.
    """
    month_ago = timezone.now() - timedelta(days=30)
    filter_combined = {"last_login__lte": month_ago} | {"last_login__isnull": True}
    inactive_users = User.objects.filter(**filter_combined).exclude(is_superuser=True)
    if inactive_users.exists():
        count = inactive_users.update(is_active=False)
        print(f"Деактивировано {count} неактивных пользователей")
    else:
        print("Нет неактивных пользователей для деактивации")
