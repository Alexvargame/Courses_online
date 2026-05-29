from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.auth.models import BaseUserManager as BUM

from courses_online.courses_online_apps.common.models import BaseModel
class BaseUserManager(BUM):

    def create_user(self, email, is_active=True, username=None, name=None, surname=None,
                    phone=None, password=None,  bonus_balance=0, is_admin=False):

        if not email:
            raise ValueError("User must have email")

        user = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            name=name,
            surname=surname,
            username=username,
            phone=phone,
            bonus_balance=bonus_balance,
            is_admin=is_admin
        )
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            password=password
        )
        user.is_admin=True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, blank=True, null=True, default='')
    surname = models.CharField(max_length=100, blank=True, null=True, default='')
    username = models.CharField(max_length=100, blank=True, null=True, default='')
    email = models.EmailField(
        verbose_name='email_address',
        max_length=255,
        unique=True,
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True, null=True, default='')
    last_login_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    bonus_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="baseuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="baseuser_set",
        related_query_name="user",
    )
    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class PromoCode(models.Model):

    name = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return self.name


class UserPromoCode(models.Model):

    user = models.ForeignKey(BaseUser, related_name="promocodes", on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, related_name="users", on_delete=models.CASCADE)

    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Промокод пользователя"
        verbose_name_plural = "Промокоды пользователя"
        unique_together = [['user', 'promo_code']]  # чтобы нельзя было активировать один код дважды


    def __str__(self):
        return f"{self.user}: {self.promo_code}"

class BonusTransaction(models.Model):

    user = models.ForeignKey(BaseUser, related_name="balance_transaction", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Изменение бонуса пользователя"
        verbose_name_plural = "Изменения бонусов пользователя"
        indexes = [models.Index(fields=['user', '-date_created'])]

    def __str__(self):
        return f"{self.user}: {self.amount}_{self.date_created}"
