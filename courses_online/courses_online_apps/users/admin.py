from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from courses_online.courses_online_apps.users.models import BaseUser, PromoCode, UserPromoCode, BonusTransaction
from courses_online.courses_online_apps.users.services import user_create

def add_bonus(modeladmin, request, queryset):
    from .models import BonusTransaction
    for user in queryset:
        BonusTransaction.objects.create(
            user=user,
            amount=100,  # сумма
            description="Ручное начисление от администратора"
        )
        user.bonus_balance += 100
        user.save()
    messages.success(request, "Бонусы начислены")

@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'surname', 'email', 'is_admin', 'registration_date',
                    'phone', 'last_login_date', 'is_active', 'bonus_balance')
    search_fields = ('email', 'user_role')
    fieldsets = (
        (None, {'fields': ('email', 'username','name', 'surname', )}),
        ('Booleans', {'fields': ('is_active','is_admin')}),
        ('Timestamps', {'fields': ('registration_date', 'last_login_date')})
    )

    readonly_fields = ('registration_date', 'last_login_date')
    actions = [add_bonus]

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)
        try:
            print('FORM_CLEAN_DATA', form.cleaned_data)
            user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(), message.ERROR)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_created', 'bonus_amount')
    search_fields = ('name',)

@admin.register(UserPromoCode)
class UserPromoCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'promo_code', 'issued_at', 'expires_at', 'is_used', 'used_at')
    list_filter = ('is_used', 'expires_at')
    search_fields = ('user__email', 'promo_code__name')

@admin.register(BonusTransaction)
class BonusTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date_created', 'description')
    list_filter = ('date_created', 'user')
    search_fields = ('user__email', 'description')
    readonly_fields = ('date_created',)