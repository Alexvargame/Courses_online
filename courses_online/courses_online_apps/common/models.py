from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    registration_date = models.DateTimeField(db_index=True, default=timezone.now)
    last_login_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


