from typing import Optional

from django.db.models.query import QuerySet

from courses_online.courses_online_apps.common.utils import get_object
from courses_online.courses_online_apps.users.filters import BaseUserFilter
from courses_online.courses_online_apps.users.models import BaseUser


def user_list(*, filters=None):
    filters = filters or {}
    qs = BaseUser.objects.all()
    return BaseUserFilter(filters, qs).qs

def user_get(user_id):
    user = get_object(BaseUser, id=user_id)
    return user


