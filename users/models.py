"""
Модели для создания объектов приложения `users`
"""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    """Кастомное создание пользователя"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Данные о платежах пользователя"""

    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
        ("card", "Оплата картой")
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="payments",
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        null=True,
        blank=True,
    )
    pay_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата платежа",
    )
    pay_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма платежа"
    )
    pay_amount_default = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    pay_method = models.CharField(
        max_length=50, choices=PAYMENT_METHODS, verbose_name="Способ оплаты"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Урок",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Id сессии",
        help_text="Укажите id сессии"
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату"
    )

    def __str__(self):
        return f"Платеж {self.session_id}: {self.user.email} - {self.pay_amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    """Подписка пользователя на курс"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscribed",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="subscribed"
    )

    def __str__(self):
        return f'User: {self.user.email} -> Course: "{self.course.name}"'

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")
