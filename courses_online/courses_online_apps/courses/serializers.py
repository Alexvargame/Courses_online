from rest_framework import serializers

from django.utils import timezone
from courses_online.courses_online_apps.payments.models import CourseAccess
from .models import Lesson, LessonProgress


class CoursesOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    bonus_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_purchased = serializers.SerializerMethodField()
    access_expires_at = serializers.SerializerMethodField()

    def get_is_purchased(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CourseAccess.objects.filter(
                user=request.user,
                course=obj,
                access_until__gt=timezone.now()
            ).exists()
        return False

    def get_access_expires_at(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            access = CourseAccess.objects.filter(
                user=request.user,
                course=obj,
                access_until__gt=timezone.now()
            ).first()
            if access:
                return access.access_until
        return None
class LessonSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    is_available =  serializers.SerializerMethodField()
    class Meta:
        model = Lesson
        fields = ('title', 'video_url', 'duration_minutes',
                  'is_free', 'is_completed', 'is_available')

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return LessonProgress.objects.filter(user=request.user,
                lesson=obj, is_completed=True).exists()
        return False

    def get_is_available(self, obj):
        if obj.is_free:
            return True
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            access = CourseAccess.objects.filter(
                user=request.user,
                course=obj.course,
                access_until__gt=timezone.now()
            ).first()
            if access:
                return True
        return False


class CoursesDetailSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    bonus_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    lessons = serializers.SerializerMethodField()

    def get_lessons(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            lessons = obj.lessons.all().order_by('order')
            if lessons:
                return LessonSerializer(lessons, many=True, context={'request': request}).data
        return []

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ('user', 'lesson', 'is_completed',
                  'completed_at')

# class CoursesProgressSerializer(serializers.Serializer):
#     lessons_completed = serializers.SerializerMethodField()
#     lessons_all = serializers.SerializerMethodField()
#     course_progress = serializers.SerializerMethodField()
#
#     def get_lessons_completed(self, obj):
#         request = self.context.get('request')
#         completed_lessons = LessonProgress.objects.filter(
#             user=request.user,
#             lesson__course=obj,
#             is_completed=True
#         ).values_list('lesson_id', flat=True).distinct()
#         return len(completed_lessons)
#     def get_lessons_all(self, obj):
#         return obj.lessons.count()
#
#     def get_course_progress(self, obj):
#         return round(self.get_lessons_completed(obj) / self.get_lessons_all(obj) * 100, 2)
#
class CoursesProgressSerializer(serializers.Serializer):
    lessons_completed = serializers.IntegerField()
    lessons_all = serializers.IntegerField()
    course_progress = serializers.FloatField()

    def to_representation(self, instance):
        request = self.context.get('request')
        # Один запрос для подсчёта пройденных уроков
        completed = LessonProgress.objects.filter(
            user=request.user,
            lesson__course=instance,
            is_completed=True
        ).values('lesson_id').distinct().count()
        total = instance.lessons.count()
        percent = round(completed / total * 100, 2) if total > 0 else 0
        return {
            'lessons_completed': completed,
            'lessons_all': total,
            'course_progress': percent,
        }