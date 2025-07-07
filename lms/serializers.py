"""
Сериализаторы приложения `lms`.
"""

from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import YouTubeLinkValidations


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация для объекта урока"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeLinkValidations(field="video")]


class CourseDetailSerializer(serializers.ModelSerializer):
    """Добавление поля вывода количества уроков"""

    numb_of_lessons = serializers.SerializerMethodField()

    @staticmethod
    def get_numb_of_lessons(instance):
        """Способ получения количества уроков"""
        return Lesson.objects.all().count()

    class Meta:
        model = Course
        fields = ("name", "description", "numb_of_lessons")


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта курса"""

    lessons = serializers.SerializerMethodField()
    numb_of_lessons = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, instance):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return instance.subscribed.filter(user=request.user).exists()
        return False

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
