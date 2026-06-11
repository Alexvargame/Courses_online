from celery import shared_task
from django.utils import timezone




import random
import time

@shared_task
def notify_new_lesson(course_id):
    time.sleep(random.randint(5, 10))
    from courses_online.courses_online_apps.payments.models import CourseAccess
    courses_access = CourseAccess.objects.filter(
        course_id=course_id,
        access_until__gt=timezone.now(),
    ).select_related('user').values_list('user__email', flat=True)
    for email in courses_access:
        # отправка email (пока print или заглушка)
        print(f"Уведомление: новый урок в курсе {course_id} для {email}")

    return f"Notified {courses_access.count()} users"

@shared_task
def deactivate_expired_access():
    time.sleep(random.randint(5, 10))
    from courses_online.courses_online_apps.payments.models import CourseAccess
    courses_access = CourseAccess.objects.filter(
        access_until__lt=timezone.now(),
    )
    for ca in courses_access:
        ca.delete()
    return f"Delete {courses_access.count()} access"
