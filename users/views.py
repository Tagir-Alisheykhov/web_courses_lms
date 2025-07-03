from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UsersSerializer


class UsersViewSet(ModelViewSet):
    """CRUD для модели Users"""

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Выбор сериализатора"""
        return UsersSerializer


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
