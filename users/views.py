"""
Представления приложения `users`.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UsersSerializer


class UserCreateAPIView(CreateAPIView):
    """Представление для создания пользователя"""

    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Переопределение полей объекта"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Отображение списка зарегистрированных пользователей"""

    serializer_class = UsersSerializer
    queryset = User.objects.all()
    filter_backends = []


class UserRetrieveAPIView(RetrieveAPIView):
    """Детальное отображение информации о пользователе"""

    serializer_class = UsersSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """Обновление данных конкретного пользователя"""

    serializer_class = UsersSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    """Обновление данных конкретного пользователя"""

    serializer_class = UsersSerializer
    queryset = User.objects.all()


class PaymentListAPIView(ListAPIView):
    """Представление списка платежей пользователя"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "pay_method",
    )
    ordering_fields = ("pay_date",)
