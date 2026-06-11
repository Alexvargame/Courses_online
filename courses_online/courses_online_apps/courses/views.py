


from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


from .serializers import CoursesOutputSerializer, CoursesDetailSerializer, LessonProgressSerializer, CoursesProgressSerializer
from .models import Course, LessonProgress, Lesson

from courses_online.courses_online_apps.payments.models import CourseAccess
from courses_online.courses_online_apps.payments.service import purchase
from courses_online.courses_online_apps.payments.serializers import PurchaseOutputSerializer
from courses_online.courses_online_apps.payments.models import Purchase
from courses_online.courses_online_apps.payments.tasks import simulate_card_payment
class CourselistApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        courses = Course.objects.all()
        serializer = CoursesOutputSerializer(courses, many=True, context={'request': request})

        return Response(serializer.data)


class CourseDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)

        serializer = CoursesDetailSerializer(course, context={'request': request})

        return Response(serializer.data)

class CoursePurchaseApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        payment_method = request.data.get('payment_method', 'bonus')
        if payment_method == 'bonus':
            purchase_course = purchase(request.user.id, pk)
            serializer = PurchaseOutputSerializer(purchase_course)
            return Response(serializer.data)
        elif payment_method == 'card':
            task = simulate_card_payment.delay(request.user.id, pk)
            return Response(
                {
                    'task_id': task.id,
                    'status': "Payment processinng",
                    },
                status=202
            )
        return  Response({"error": "Invalid paymennt method"}, status=400)


class LessonCompletedApiview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, id=pk)
        if lesson.is_free:
            progress, created = LessonProgress.objects.get_or_create(
                user=request.user,
                lesson=lesson,
                defaults={'is_completed': True, 'completed_at': timezone.now()}
            )
            if not created and progress.is_completed:
                return Response({"error": "Lesson already completed"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = LessonProgressSerializer(progress)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        if not CourseAccess.objects.filter(user=request.user, course=lesson.course).exists():
            return Response({"error": "The Course is not purchsed"}, status=status.HTTP_403_FORBIDDEN)

        if CourseAccess.objects.filter(user=request.user, course=lesson.course).first().access_until >= timezone.now():
            if not LessonProgress.objects.filter(user=request.user, lesson=lesson).exists():
                lesson_progress = LessonProgress.objects.create(
                    user=request.user,
                    lesson=lesson,
                    is_completed=True,
                    completed_at=timezone.now()
                )
                serializer = LessonProgressSerializer(lesson_progress)
                return Response(serializer.data)
            return Response({"error": "User already made this lesson"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "The course is not available"}, status=status.HTTP_403_FORBIDDEN)

class CourseProgressApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        access = CourseAccess.objects.filter(user=request.user, course=course).first()
        if not access:
            return Response({"error": "The Course is not purchsed"}, status=status.HTTP_403_FORBIDDEN)

        if access.access_until >= timezone.now():
            serializer = CoursesProgressSerializer(course, context={'request': request})
            return Response(serializer.data)
        return Response({"error": "The course is not available"}, status=status.HTTP_403_FORBIDDEN)


