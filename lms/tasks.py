"""
Celery задачи
"""

import os

from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.urls import reverse
from dotenv import load_dotenv

from lms.models import Course
from users.models import Subscription

load_dotenv()

sender = os.getenv("EMAIL_HOST_USER")
main_page = os.getenv("MAIN_PAGE")


@shared_task
def course_update_notification(course_id) -> None:
    """Оповещений подписчиков курсов на обновление уроков"""
    try:
        course = Course.objects.get(pk=course_id)
        subscriptions = Subscription.objects.filter(course_id=course_id)
        recipients = [sub.user.email for sub in subscriptions if sub.user.email]
        if not recipients:
            print(f"Нет подписчиков для курса {course_id}")
            return
        current_site = get_current_site(None)
        domain = current_site.domain
        course_url = reverse("lms:courses-detail", kwargs={"pk": course_id})
        full_url = f"http://{domain}{course_url}"
        send_mail(
            subject=f"Обновление курса '{course.name}'",
            message=f"Курс обновился.\nПерейдите по ссылке для просмотра: {full_url}",
            from_email=sender,
            recipient_list=recipients,
        )
        print(f"Уведомления отправлены {len(recipients)} подписчикам курса {course_id}")
    except ObjectDoesNotExist:
        print(f"Курс {course_id} не найден")
    except Exception as err:
        print(f"Ошибка при отправке уведомлений: {str(err)}")
