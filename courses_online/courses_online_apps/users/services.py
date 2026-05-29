from django.db import transaction
from django.utils import timezone

from courses_online.courses_online_apps.users.models import BaseUser, BonusTransaction, UserPromoCode


@transaction.atomic
def user_create(*, email, username, name=None, surname=None, phone=None, is_active=True, is_admin=False,
                password=None, bonus_balance=0):
    print(email, username, name, surname, phone, is_active, is_admin, user_role)
    user = BaseUser.objects.create_user(email=email, username=username, name=name, surname=surname,
                                        phone=phone, is_active=is_active, bonus_balance=bonus_balance, password=password)
    return user

@transaction.atomic
def change_bonus_balance(user_id, user_promocode_id, description, action):
    user = BaseUser.objects.select_for_update().get(id=user_id)
    user_promocode = UserPromoCode.objects.get(id=user_promocode_id)
    if user_promocode.is_used:
        raise ValueError ("PromoCode already used")
    if user_promocode.expires_at < timezone.now():
        raise ValueError("PromoCode is not valid")
    if action == "crediting bonuses":
        amount = user_promocode.promo_code.bonus_amount
    elif action == "deducting bonuses":
        amount = -user_promocode.promo_code.bonus_amount
    bonus_transaction = BonusTransaction.objects.create(
        user=user,
        amount=amount,
        description=description
    )
    user_promocode.is_used = True
    user_promocode.save()
    user.bonus_balance += amount
    user.save()
    return bonus_transaction

