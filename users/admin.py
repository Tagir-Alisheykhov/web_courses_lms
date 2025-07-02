from django.contrib import admin

from users.models import Payment, User


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
        "paid_course",
        "paid_lesson",
    ]
    list_filter = ["pay_date", "pay_amount", "pay_method"]
    search_fields = [
        "user",
        "pay_date",
        "pay_amount",
        "pay_method",
        "paid_course",
        "paid_lesson",
    ]
