"""
Конечные точки приложения `users`.
"""

from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentListAPIView, UserCreateAPIView,
                         UserDestroyAPIView, UserListAPIView,
                         UserRetrieveAPIView, UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    # model User
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="user_login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("register/", UserCreateAPIView.as_view(), name="user_register"),
    path("", UserListAPIView.as_view(), name="users"),
    path("detail/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_delete"),
    # model Payment
    path("payments/", PaymentListAPIView.as_view(), name="payments"),
]
