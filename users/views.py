"""
Представления приложения `users`.
"""

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course
from users.models import Payment, Subscription, User
from users.serializers import PaymentSerializer, UsersSerializer


class SubscriptionAPIView(APIView):
    """Управление подпиской пользователя на курс"""

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        """Работа с объектом модели подписки"""
        course_id = kwargs.get("pk")
        if not course_id:
            return Response({"error": "Не указан `course_id`"}, status=400)
        course_item = get_object_or_404(Course, id=course_id)
        current_user = request.user
        subs_item = Subscription.objects.filter(user=current_user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
            is_subscribed = False
        else:
            Subscription.objects.create(user=current_user, course=course_item)
            message = "Подписка добавлена"
            is_subscribed = True
        return Response({"message": message, "is_subscribed": is_subscribed})


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

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
