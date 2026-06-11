from django.urls import path

from .views import (
    CourselistApiView, CourseDetailApiView,
    CoursePurchaseApiView, LessonCompletedApiview,
    CourseProgressApiView,
)

app_name = 'courses'
urlpatterns =[

    path("courses/", CourselistApiView.as_view(), name="courses_list"),
    path("courses/<int:pk>/", CourseDetailApiView.as_view(), name="course_detail"),
    path("courses/<int:pk>/purchase/", CoursePurchaseApiView.as_view(), name="course_purchase"),
    path("lessons/<int:pk>/complete/", LessonCompletedApiview.as_view(), name='lessonn_copleted'),
    path("courses/<int:pk>/progress/", CourseProgressApiView.as_view(), name="course_progress"),
]