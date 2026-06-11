

from django.urls import path, include

urlpatterns = [

    path('users/', include(('courses_online.courses_online_apps.users.urls', 'users'), namespace='users')),
    path('courses/', include(('courses_online.courses_online_apps.courses.urls', 'courses'), namespace='courses')),
    path('payments/', include(('courses_online.courses_online_apps.payments.urls', 'payments'), namespace='payments')),


]
