from django.shortcuts import render
from django.http import Http404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response

from .serializers import UserOutputSerializer, UserInputSerializer, BonusTransactionsSerializer
from .models import PromoCode, UserPromoCode, BonusTransaction
from .services import change_bonus_balance_by_promocode
# from .selectors import get_object
class UserDetailApi( APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user is None:
            raise Http404
        serializer = UserOutputSerializer(request.user)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateApi(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        print("POST")
        serializer = UserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)


class ActivatePromoCodeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        promo_code = PromoCode.objects.filter(name=request.data['promo_code']).first()
        if not promo_code:
            return Response({"error": "PromoCode is not exists"}, status=status.HTTP_403_FORBIDDEN)

        print(promo_code)
        if UserPromoCode.objects.filter(user=request.user, promo_code=promo_code).exists():
            user_promo_code = UserPromoCode.objects.filter(user=request.user,promo_code=promo_code).first()
            if user_promo_code.is_used or user_promo_code.expires_at < timezone.now():
                return Response({"error": "PromoCode already used or not in use "}, status=status.HTTP_403_FORBIDDEN)
        else:
            user_promo_code = UserPromoCode.objects.create(
                user = request.user,
                promo_code = promo_code,
                expires_at=timezone.now() + relativedelta(years=1),
            )

        change_bonus_balance_by_promocode(request.user.id, user_promo_code.id, promo_code.name, "crediting bonuses")
        return Response(status=201)


class BonusTransactionsHistoryApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        bonus_transactions = BonusTransaction.objects.filter(user=request.user)
        serializer = BonusTransactionsSerializer(bonus_transactions, many=True)

        return Response(serializer.data)

