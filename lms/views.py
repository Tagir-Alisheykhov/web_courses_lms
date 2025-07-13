"""
Конечные точки приложения `lms`
"""
from datetime import timedelta

from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.paginators import CustomPagination
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from lms.tasks import course_update_notification
from users.permissions import IsModer, IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Это тестовое описание для эндпоинта"
    ),
)
class CourseViewSet(ModelViewSet):
    """CRUD для модели курса."""

    queryset = Course.objects.all()
    filter_backends = []
    pagination_class = CustomPagination

    def get_serializer_context(self):
        """Добавление request в контекст сериализатора."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_permissions(self):
        """Проверка прав доступа пользователя."""
        if self.request.user.is_superuser:
            return [IsAdminUser()]
        if self.action == "create":
            self.permission_classes = (~IsModer, IsAuthenticated)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner, IsAuthenticated)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | ~IsModer, IsAuthenticated)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Привязка курса к его создателю."""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Отправка уведомлений после обновления курса"""
        instance = serializer.save()
        old_last_update = Course.objects.get(pk=instance.pk).last_update
        if old_last_update < timezone.now() - timedelta(hours=4):
            course_update_notification.delay(instance.id)

    def get_serializer_class(self):
        """Выбор сериализатора"""
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer


class LessonCreateAPIView(CreateAPIView):
    """Представление для создания объекта урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        """Привязка урока к его создателю"""
        lesson = serializer.save(owner=self.request.user)
        lesson.course.last_update = timezone.now()
        lesson.course.save()


class LessonListAPIView(ListAPIView):
    """Представление списка объектов уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = []
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    """Получение объекта урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)
    filter_backends = []


class LessonUpdateAPIView(UpdateAPIView):
    """Представление для изменения объекта урок"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)
    filter_backends = []

    def perform_update(self, serializer):
        """Отправка уведомления, если урок был обновлен"""
        lesson = serializer.save()
        lesson.course.last_update = timezone.now()
        lesson.course.save()
        old_last_update = Course.objects.get(pk=lesson.course.pk).last_update
        if old_last_update < timezone.now() - timedelta(hours=4):
            course_update_notification.delay(lesson.course.id)


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление объекта урок"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
    filter_backends = []

    def perform_destroy(self, instance):
        """Фиксация изменения урока"""
        course = instance.course
        instance.delete()
        course.last_update = timezone.now()
        course.save()
