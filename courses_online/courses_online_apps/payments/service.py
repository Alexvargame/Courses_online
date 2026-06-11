from decimal import Decimal

from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .models import CourseAccess, Purchase
from courses_online.courses_online_apps.users.models import BaseUser, BonusTransaction
from courses_online.courses_online_apps.users.services import change_bonus_balance_by_purchase
from courses_online.courses_online_apps.courses.models import Course

def check_access_to_course(user_id, course_id):

    user = BaseUser.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)

    access_course = CourseAccess.objects.filter(user=user, course=course).first()
    if access_course:
        if access_course.access_until >= timezone.now():
            return True
    return False

def purchase(user_id, course_id):

    bonus = Decimal(5) / Decimal(100)

    user = BaseUser.objects.select_for_update().get(id=user_id)
    course = Course.objects.get(id=course_id)

    if Purchase.objects.filter(user=user, course=course).first():
        raise ValueError("User already baut this course")
    purchase = Purchase.objects.create(user=user, course=course)

    if course.bonus_price:
        if user.bonus_balance >= course.bonus_price:
            user.bonus_balance -= course.bonus_price
            amount_bonus = course.bonus_price
            amount_paid = 0

        else:
            amount_paid = course.price - user.bonus_balance
            amount_bonus = user.bonus_balance
            user.bonus_balance = 0
            user.bonus_balance += amount_paid * bonus
        change_bonus_balance_by_purchase(user, amount_bonus, f"Purchase {purchase}",
                                         "deducting bonuses")
        if amount_paid:
            change_bonus_balance_by_purchase(user, amount_paid * bonus, f"Purchase {purchase}",
                                             "crediting bonuses")
        user.save()

        purchase.paid_with_bonus = True
        purchase.amount_paid = amount_paid
        purchase.save()


    else:
        purchase.amount_paid = course.price
        purchase.save()
        user.bonus_balance += course.price * bonus
        change_bonus_balance_by_purchase(user, course.price * bonus, f"Purchase {purchase}",
                                         "crediting bonuses")
        user.save()

    if CourseAccess.objects.filter(user=user, course=course).exists():
        raise ValueError("User already has access to this course")
    accses_course = CourseAccess.objects.create(
        user=user,
        course=course,
        access_until=timezone.now()+ relativedelta(years=1),
        is_active=True
    )
    return purchase

