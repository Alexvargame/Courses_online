from django.contrib import admin

from .models import Course, Lesson, LessonProgress


class LessonInline(admin.TabularInline):  # или StackedInline
    model = Lesson
    extra = 1  # пустых строк для добавления
    fields = ('title', 'order', 'duration_minutes', 'is_free', 'video_url')
    ordering = ('order',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'description', 'price', 'bonus_price',
    'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('title',)
    inlines = [LessonInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    list_display = ('id', 'course', 'title', 'video_url',
    'duration_minutes', 'order', 'is_free' )


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'lesson', 'is_completed', 'completed_at')
