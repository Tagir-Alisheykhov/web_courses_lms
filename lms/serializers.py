from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализация для объекта урока"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Добавление поля вывода количества уроков"""

    numb_of_lessons = SerializerMethodField()

    @staticmethod
    def get_numb_of_lessons(instance):
        """Способ получения количества уроков"""
        return Lesson.objects.all().count()

    class Meta:
        model = Course
        fields = ("name", "description", "numb_of_lessons")


class CourseSerializer(ModelSerializer):
    """Сериализатор для объекта курса"""

    lessons = SerializerMethodField()
    numb_of_lessons = SerializerMethodField()

    @staticmethod
    def get_lessons(instance):
        """Вывод поля списка уроков"""
        lessons = instance.lesson.all()
        return LessonSerializer(lessons, many=True).data

    @staticmethod
    def get_numb_of_lessons(instance):
        """Вывод количества уроков"""
        return instance.lesson.count()

    class Meta:
        model = Course
        fields = "__all__"
