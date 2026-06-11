from django.db import models

from courses_online.courses_online_apps.users.models import BaseUser
from courses_online.courses_online_apps.courses.models import Course

class  Purchase(models.Model):

    user = models.ForeignKey(BaseUser, related_name='purchases', on_delete=models.CASCADE)
    course = models.ForeignKey(Course,  on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    paid_with_bonus = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Покупка курса"
        verbose_name_plural = "Покупки курсов"

    def __str__(self):
        return f"{self.user}_{self.course}"


class CourseAccess(models.Model):
    user = models.ForeignKey(BaseUser, related_name='user_accesses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course_accesses', on_delete=models.CASCADE)
    access_until = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Доступ к курсу"
        verbose_name_plural = "Доступы к курсам"
        unique_together = [['user', 'course']]

    def __str__(self):
        return f"{self.user}_{self.course}: {self.access_until}"