"""
Тестирование приложения `users`
"""

from django.urls import reverse
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import User, Subscription


class SubscriptionTestCase(APITestCase):
    """Тестирование http-методов модели Lesson"""

    def setUp(self):
        """Тестовые данные"""
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="SkyProCourse", owner=self.user)
        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        """Изменения статуса при подписке на курс (True/False)"""
        # self.course.subscribed = False
        url = reverse("users:subscribe", args=(self.course.pk,))
        response_subscribe_false = self.client.post(url)
        self.assertFalse(response_subscribe_false.json()["is_subscribed"])
        response_subscribe_true = self.client.post(url)
        self.assertTrue(response_subscribe_true.json()["is_subscribed"])
