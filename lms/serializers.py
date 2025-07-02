from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Сериализатор для объекта курса"""

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Добавление поля вывода количества уроков"""

    numb_of_lessons = SerializerMethodField()

    @staticmethod
    def get_numb_of_lessons(obj):
        """Способ получения количества уроков"""
        return Lesson.objects.all().count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'numb_of_lessons')


class LessonSerializer(ModelSerializer):
    """Сериализация для объекта урока"""

    class Meta:
        model = Lesson
        fields = "__all__"
