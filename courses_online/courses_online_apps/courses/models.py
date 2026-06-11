from django.db import models

from courses_online.courses_online_apps.users.models import BaseUser
from .tasks import notify_new_lesson
class Course(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title}: {self.created_at}"


class Lesson(models.Model):


    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title  = models.CharField(max_length=50)
    video_url = models.URLField(blank=True)
    duration_minutes = models.IntegerField()
    order = models.IntegerField()
    is_free = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['order']

    def __str__(self):
        return f"{self.title}: {self.course}"

    def save(self, *args, **kwargs):
        is_new = not self.pk  # если объекта ещё нет в БД
        super().save(*args, **kwargs)
        if is_new:
            notify_new_lesson.delay(self.course.id)

class LessonProgress(models.Model):

    user = models.ForeignKey(BaseUser, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,  on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name = "Пройденный урок"
        verbose_name_plural = "Пройденные уроки"
        indexes = [models.Index(fields=['user', 'lesson'])]

    def __str__(self):
        return f"{self.user}_{self.lesson}: {self.completed_at}"