"""
Утилиты приложения `users`
"""
import stripe
from currency_converter import CurrencyConverter
from rest_framework import status
from rest_framework.response import Response

from config.settings import STRIPE_API_KEY_SECRET


stripe.api_key = STRIPE_API_KEY_SECRET


def conv_rub_to_usd(amount: int = 1) -> float:
    """Конвертация из рубля в доллар."""
    c = CurrencyConverter()
    rate = c.convert(amount, "RUB", "USD")
    return rate


def create_stripe_product(product_id, product_name, default_price=None):
    """Создание продукта в `stripe` с ценой"""
    product_data = {
        "id": f"prod_{product_id}",
        "name": product_name
    }
    if default_price is not None or default_price != 0:
        product_data["default_price_data"] = {
            "unit_amount": int(default_price * 100),
            "currency": "usd"
        }
    product = stripe.Product.create(**product_data)
    return product.id, product


def create_stripe_price(amount, product_id, set_as_default=False):
    """Создает цену в `stripe`"""
    price = stripe.Price.create(
        unit_amount=int(amount * 100),
        product=product_id,
        currency="usd",
    )
    if set_as_default is True:
        stripe.Product.modify(
            product_id,
            default_price=price.id
        )
    return price


def create_stripe_session(price_id):
    """Создание сессии для оплаты в `stripe`"""
    session = stripe.checkout.Session.create(
        mode="payment",
        success_url="https://127.0.0.1:8000/",
        cancel_url="https://127.0.0.1:8000/",
        line_items=[{
            "price": price_id,  # Принимаем просто строку с ID цены
            "quantity": 1,
        }],
    )
    return session.get("id"), session.get("url")


def get_product_from_stripe(prod_id: str) -> Response:
    """Получение информации об одном продукте из `stripe` с данными о цене"""
    try:
        product = stripe.Product.retrieve(prod_id)
        price_data = None
        if product.default_price:
            price = stripe.Price.retrieve(product.default_price)
            price_data = {
                "id": price.id,
                "unit_amount": price.unit_amount / 100,  # Конвертируем обратно в доллары
                "currency": price.currency
            }
        return Response({
            "id": product.id,
            "name": product.name,
            "default_price": price_data,  # Теперь это объект с данными о цене
            "active": product.active,
            "created": product.created,
            # остальные поля по необходимости
        }, status=status.HTTP_200_OK)
    except stripe.error.InvalidRequestError as err:
        return Response(
            {"error": f"Product not found in Stripe: {str(err)}"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as err:
        return Response(
            {"error": f"Stripe API error: {str(err)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_stripe_product(prod_id: str):
    """Получение продукта из Stripe (возвращает объект Stripe)"""
    try:
        return stripe.Product.retrieve(prod_id)
    except stripe.error.InvalidRequestError as err:
        print(f"Stripe product error: {str(err)}")
        raise
