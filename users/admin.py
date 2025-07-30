"""
Настройка админ панели для приложения `users`.
"""

from django.contrib import admin

from users.models import Payment, Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Создание пользователя в админке"""

    list_display = ["email", "city", "username", "avatar", "phone"]
    list_filter = ["city", "email"]
    search_fields = ["email", "phone", "city"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Создание пользователя в админке"""

    list_display = [
        "user",
        "pay_date",
        "pay_amount",
        "pay_method",
        "course",
        "lesson",
        "session_id",
        "link",
    ]
    list_filter = ["pay_date", "pay_amount", "pay_method"]
    search_fields = [
        "user",
        "pay_date",
        "pay_amount",
        "pay_method",
        "course",
        "lesson",
    ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Отображение данных о подписках в админ-панели"""

    list_display = (
        "user",
        "course",
    )
    list_filter = ("course",)
    search_fields = (
        "user",
        "course",
    )
