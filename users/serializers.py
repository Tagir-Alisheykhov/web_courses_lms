"""
Сериализаторы приложения `users` .
"""

from rest_framework import serializers

from users.models import Payment, User, Subscription


# class SubscriptionSerializer(serializers.ModelSerializer):
#     """Сериализация для модели Subscription"""
#
#     is_signed = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Subscription
#         fields = ("user", "course", "is_signed")
#
#     def get_is_signed(self, instance):
#         """
#         Проверяем подписку пользователя на курс.
#         """
#         request = self.context.get("request")
#         if request and request.user.is_authenticated:
#             return Subscription.objects.filter(
#                 user=request.user,
#                 course=instance.course
#             ).exists()
#         return False


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализация модели Платежи"""

    class Meta:
        model = Payment
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    class Meta:
        model = User
        fields = "__all__"
