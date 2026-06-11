from rest_framework import serializers
from .models import BaseUser, UserPromoCode, BonusTransaction


class UserOutputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    name = serializers.CharField()
    surname = serializers.CharField()
    phone = serializers.CharField()
    bonus_balance = serializers.CharField()


class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email', 'password', 'username', 'name', 'surname', 'phone', 'is_admin', 'is_active', 'bonus_balance']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = BaseUser(**validated_data)
        user.set_password(password)  # хеширование пароля
        user.save()
        return user

class UserPromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPromoCode
        fields = ('user', 'promo_code', 'expires_at')


class BonusTransactionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BonusTransaction
        fields = ('id', 'user', 'amount', 'date_created', 'description')