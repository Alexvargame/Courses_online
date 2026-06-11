from rest_framework import serializers

from .models import Purchase, CourseAccess


class PurchaseOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('user', 'course', 'purchased_at',
                  'paid_with_bonus', 'amount_paid')

class CourseAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAccess
        fields = ('id', 'user', 'course',
                  'access_untill', 'is_active')