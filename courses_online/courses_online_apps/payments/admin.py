from django.contrib import admin

from .models import Purchase, CourseAccess


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'purchased_at', 'paid_with_bonus', 'amount_paid')
    list_filter = ('paid_with_bonus', 'purchased_at', 'course')
    search_fields = ('user__email', 'course__title')
    readonly_fields = ('purchased_at',)


@admin.register(CourseAccess)
class CourseAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'access_until', 'is_active')
    list_filter = ('access_until', 'course')
    search_fields = ('user__email', 'course__title')

    def is_active(self, obj):
        from django.utils import timezone
        return obj.access_until > timezone.now()

    is_active.boolean = True