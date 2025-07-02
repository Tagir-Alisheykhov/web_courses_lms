from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UsersViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UsersViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments"),
]

urlpatterns += router.urls
