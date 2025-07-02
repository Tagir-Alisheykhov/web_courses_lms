from django.core.management.base import BaseCommand
from users.models import User, Payment
from lms.models import Course, Lesson


class Command(BaseCommand):
    """Тестовые данные для наполнения БД"""

    help = "Создает тестовые данные: пользователя, курс, урок и платежи"

    def handle(self, *args, **kwargs):
        # 1. Создание пользователя
        email = "your@email.com"
        if not User.objects.filter(email=email).exists():
            user = User.objects.create(
                email=email,
                password="123456",
                phone="+79001234567",
                city="Москва"
            )
            self.stdout.write(f" ✅ Пользователь создан: {user.email}")
        else:
            user = User.objects.get(email=email)
            self.stdout.write(f" ℹ️ Пользователь уже существует: {user.email}")

        # 2. Создание курса
        course_name = "Основы программирования"
        if not Course.objects.filter(name=course_name).exists():
            course = Course.objects.create(
                name=course_name,
                description="Курс для начинающих программистов."
            )
            self.stdout.write(f" ✅ Курс создан: {course.name}")
        else:
            course = Course.objects.get(title=course_name)
            self.stdout.write(f" ℹ️ Курс уже существует: {course.name}")

        # 3. Создание урока
        lesson_name = "Введение в Python"
        if not Lesson.objects.filter(name=lesson_name).exists():
            lesson = Lesson.objects.create(
                name=lesson_name,
                description="Первый урок по языку Python.",
                course=course
            )
            self.stdout.write(f" ✅ Урок создан: {lesson.name}")
        else:
            lesson = Lesson.objects.get(title=lesson_name)
            self.stdout.write(f" ℹ️ Урок уже существует: {lesson.name}")

        # 4. Создание платежа за курс
        payment_course, created = Payment.objects.get_or_create(
            user=user,
            paid_course=course,
            defaults={
                "pay_amount": 10000.00,
                "pay_method": "transfer"
            }
        )
        if created:
            self.stdout.write(f" ✅ Платеж за курс создан: {payment_course.pay_amount}")
        else:
            self.stdout.write(" ℹ️ Платеж за курс уже существует")

        # 5. Создание платежа за урок
        payment_lesson, created = Payment.objects.get_or_create(
            user=user,
            paid_lesson=lesson,
            defaults={
                "pay_amount": 1500.00,
                "pay_method": "cash"
            }
        )
        if created:
            self.stdout.write(f" ✅ Платеж за урок создан: {payment_lesson.pay_amount}")
        else:
            self.stdout.write(" ℹ️ Платеж за урок уже существует")

        # self.stdout.write(self.style.SUCCESS("✅ Все тестовые данные успешно загружены!"))
