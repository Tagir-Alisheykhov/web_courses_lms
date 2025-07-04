"""
Сериализаторы приложения `users` .
"""

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """Сериализация модели Платежи"""

    class Meta:
        model = Payment
        fields = "__all__"


class UsersSerializer(ModelSerializer):
    """Сериализатор для модели User"""

    class Meta:
        model = User
        fields = "__all__"
