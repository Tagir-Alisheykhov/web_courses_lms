"""
Тестирование приложения `lms`.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course
from users.models import User, Subscription


class LessonTestCase(APITestCase):
    """Тестирование http-методов модели Lesson"""

    def setUp(self):
        """Тестовые данные"""
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="SkyProCourse", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="SkyProLesson", course=self.course, owner=self.user
        )
        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Детальное отображение урока"""
        url = reverse("lms:get_lesson", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Создание урока"""
        url = reverse("lms:create_lesson")
        data = {"name": "Сериализаторы"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Обновление урока"""
        url = reverse("lms:edit_lesson", args=(self.lesson.pk,))
        data = {"name": "Сериализаторы"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Сериализаторы")

    def test_lesson_delete(self):
        """Обновление урока"""
        url = reverse("lms:delete_lesson", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Список уроков"""
        url = reverse("lms:lessons")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "video": self.lesson.video,
                    "course": 3,
                    "owner": 3,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
