"""
Конечные точки приложения `lms`
"""

from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.paginators import CustomPagination
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from users.permissions import IsModer, IsOwner


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
        serializer.save(owner=self.request.user)


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


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление объекта урок"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
    filter_backends = []
