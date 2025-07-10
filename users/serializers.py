"""
Сериализаторы приложения `users` .
"""

from rest_framework import serializers

from users.models import Payment, User


class PaymentListSerializer(serializers.ModelSerializer):
    """Получение списка платежей из базы данных приложения"""

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentStripeRetrieveSerializer(serializers.ModelSerializer):
    """Получение детальной информации о платеже по id, напрямую из сервиса Stripe"""

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализация модели Платежи"""

    class Meta:
        model = Payment
        fields = "__all__"

    def validate(self, data):
        """Проверка на то, что выбран либо курс, либо урок"""
        if data.get("course") and data.get("lesson"):
            raise serializers.ValidationError("Выберите либо курс, либо урок, но не оба сразу.")
        if not data.get("course") and not data.get("lesson"):
            raise serializers.ValidationError("Необходимо выбрать либо курс, либо урок.")
        return data


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    class Meta:
        model = User
        fields = "__all__"