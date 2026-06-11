from celery import shared_task
from django.utils import timezone

from .models import Purchase, CourseAccess
from courses_online.courses_online_apps.users.models import BaseUser
from courses_online.courses_online_apps.courses.models import Course
import random
import time

@shared_task
def simulate_card_payment(user_id, course_id):
    time.sleep(random.randint(5, 10))

    if random.random() > 0.95:
        raise Exception("Payment failed")

    user = BaseUser.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)
    purchase, created = Purchase.objects.get_or_create(
        user=user,
        course=course,
        defaults={
            'amount_paid': course.price,
            'paid_with_bonus': False
        }
    )

    CourseAccess.objects.create(
        user=user,
        course=course,
        access_until=timezone.now() + timezone.timedelta(days=365),
        is_active=True
    )
    bonus_amount = course.price * Decimal('0.05')
    user.bonus_balance += bonus_amount
    user.save()

    return {"status": "success", "purchase_id": purchase.id}