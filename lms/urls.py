from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateAPIView,
                       LessonDestroyAPIView, LessonListAPIView,
                       LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = LmsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="get_lesson"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="create_lesson"),
    path(
        "lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="delete_lesson"
    ),
    path("lessons/edit/<int:pk>/", LessonUpdateAPIView.as_view(), name="edit_lesson"),
]

urlpatterns += router.urls
