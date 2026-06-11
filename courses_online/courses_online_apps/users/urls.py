from django.urls import path

from .views import UserDetailApi, UserCreateApi, ActivatePromoCodeApiView, BonusTransactionsHistoryApiView

app_name = 'users'
urlpatterns =[
    path('me/', UserDetailApi.as_view(), name='me_detail'),
    path('register/', UserCreateApi.as_view(), name='user_register'),
    path('bonus/activate_promo/', ActivatePromoCodeApiView.as_view(), name='promo_active'),
    path('bonus/history/', BonusTransactionsHistoryApiView.as_view(), name='bonus_history'),
]