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
from stripe import InvalidRequestError

from lms.models import Course
from users.models import Payment, Subscription, User
from users.serializers import (PaymentListSerializer, PaymentSerializer,
                               PaymentStripeRetrieveSerializer,
                               UsersSerializer)
from users.services import (conv_rub_to_usd, create_stripe_price,
                            create_stripe_product, create_stripe_session,
                            get_product_from_stripe, get_stripe_product)


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
    """Получение списка платежей из базы данных приложения"""

    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = (
        "course",
        "lesson",
        "pay_method",
    )
    ordering_fields = ("pay_date",)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        """
        Обработка объекта.
        Создание продукта и цены (если не существуют).
        Создание сессии и ссылки на оплату.
        Body (для создания платежа):
        "pay_amount": int: <amount>,
        "pay_method": str: <card/cash/transfer>,
        "course": int: <course_id>
        "pay_amount_default": int: <amount> (optional)
        """
        payment = serializer.save(user=self.request.user)
        product = payment.course if payment.course else payment.lesson
        base_amount = (
            payment.pay_amount_default or 0
            if not payment.pay_amount or payment.pay_amount == 0
            else payment.pay_amount
        )
        amount_in_dollars = conv_rub_to_usd(base_amount)
        try:
            product_id_stripe, product_obj = create_stripe_product(
                product_id=str(product.id),
                product_name=product.name,
                default_price=amount_in_dollars,
            )
        except InvalidRequestError:
            product_id_stripe = f"prod_{product.id}"
            product_obj = get_stripe_product(product_id_stripe)
        price_id = product_obj.default_price
        if not price_id:
            price_id = create_stripe_price(
                amount=amount_in_dollars,
                product_id=product_id_stripe,
            )
        session_id, payment_link = create_stripe_session(price_id=price_id)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentStripeRetrieveAPIView(RetrieveAPIView):
    """Получение детальной информации о платеже из сервиса Stripe"""

    serializer_class = PaymentStripeRetrieveSerializer
    queryset = Payment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """Получение информации об объекте"""
        prod_id = f"prod_{kwargs.get('pk')}"
        return get_product_from_stripe(prod_id)
