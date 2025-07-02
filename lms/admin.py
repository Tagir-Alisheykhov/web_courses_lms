from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Раздел с курсами в админке"""

    list_display = ("name", "description", "preview")
    search_fields = ("name", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Раздел с уроками в админке"""

    list_display = ("name", "description", "preview", "video", "course")
    search_fields = ("name", "description")
