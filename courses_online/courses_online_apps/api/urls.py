

from django.urls import path, include

urlpatterns = [

    path('users/', include(('courses_online.courses_online_apps.users.urls', 'users'), namespace='users')),

]
