"""
Модели для создания объектов приложения `lms`
"""

from django.db import models


class Course(models.Model):
    """Модель учебного курса"""

    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
    )
    preview = models.ImageField(
        upload_to="lms/previews/", blank=True, null=True, verbose_name="Превью"
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        help_text="Укажите создателя курса",
        verbose_name="Создатель курса",
        null=True,
        blank=True,
    )
    last_update = models.DateTimeField(
        auto_now=True, verbose_name="последнее обновление"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока"""

    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.CharField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Введите описание урока",
    )
    preview = models.ImageField(
        upload_to="lms/previews/", blank=True, null=True, verbose_name="Превью"
    )
    video = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видео",
    )
    course = models.ForeignKey(
        Course,
        related_name="lesson",
        on_delete=models.SET_NULL,
        verbose_name="Название курса",
        help_text="Выберите курс",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        help_text="Укажите создателя урока",
        verbose_name="Создатель урока",
        null=True,
        blank=True,
    )
    last_update = models.DateTimeField(
        auto_now=True, verbose_name="последнее обновление"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
