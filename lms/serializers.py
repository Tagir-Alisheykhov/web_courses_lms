from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Сериализатор для объекта курса"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """Сериализация для объекта урока"""

    class Meta:
        model = Lesson
        fields = "__all__"
