"""
Кастомные валидаторы приложения `lms`.
"""

import re

from rest_framework.serializers import ValidationError


class YouTubeLinkValidations:
    """Валидация на то, что ссылка ведет на YouTube"""

    def __init__(self, field):
        """Получение ссылки"""
        self.field = field

    def __call__(self, value):
        """Логика проверки ссылки"""
        url = dict(value).get(self.field)
        if not url:
            return
        pattern = r"^https?://(www\.)?youtube\.com/.+$"
        if not re.match(pattern, url):
            raise ValidationError("Ссылка должна быть только на YouTube (youtube.com).")
