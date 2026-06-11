import os
import django
from datetime import datetime
import sys
sys.path.insert(0, r'C:\Python311\django\courses_online')

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "courses_online.config.django.base")

django.setup()

from courses_online.courses_online_apps.courses.models import Course, Lesson

now = datetime.now()

# Курс 1: Python для начинающих
course1, created1 = Course.objects.get_or_create(
    title="Python для начинающих",
    defaults={
        "description": "Базовый курс по Python с нуля. Изучите синтаксис, функции, списки, словари и основы ООП.",
        "price": 100.00,
        "bonus_price": 80.00,
        "created_at": now,
        "updated_at": now,
    }
)

if created1:
    print(f"Создан курс: {course1.title}")
else:
    print(f"Курс уже существует: {course1.title}")

# Уроки для курса 1
lessons1 = [
    (1, "Установка Python и IDE", 15, True),
    (2, "Переменные и типы данных", 25, True),
    (3, "Условные операторы", 30, False),
    (4, "Циклы for и while", 35, False),
    (5, "Функции", 40, False),
]

for order, title, duration, is_free in lessons1:
    lesson, created = Lesson.objects.get_or_create(
        course=course1,
        order=order,
        defaults={
            "title": title,
            "duration_minutes": duration,
            "is_free": is_free,
            "video_url": f"https://example.com/lesson{order}",
        }
    )
    if created:
        print(f"  Создан урок: {title}")
    else:
        print(f"  Урок уже существует: {title}")

# Курс 2: Django для профи
course2, created2 = Course.objects.get_or_create(
    title="Django для профи",
    defaults={
        "description": "Продвинутый курс по Django: ORM, миграции, аутентификация, REST API, деплой.",
        "price": 200.00,
        "bonus_price": 160.00,
        "created_at": now,
        "updated_at": now,
    }
)

if created2:
    print(f"Создан курс: {course2.title}")
else:
    print(f"Курс уже существует: {course2.title}")

# Уроки для курса 2
lessons2 = [
    (1, "Основы Django ORM", 45, True),
    (2, "Миграции и модели", 50, False),
    (3, "View и URL диспетчер", 40, False),
    (4, "DRF сериализаторы", 55, False),
]

for order, title, duration, is_free in lessons2:
    lesson, created = Lesson.objects.get_or_create(
        course=course2,
        order=order,
        defaults={
            "title": title,
            "duration_minutes": duration,
            "is_free": is_free,
            "video_url": f"https://example.com/lesson{order+5}",
        }
    )
    if created:
        print(f"  Создан урок: {title}")
    else:
        print(f"  Урок уже существует: {title}")

print("\n✅ Готово! Курсы и уроки добавлены.")