"""Admin registration for StudyFlow models."""
from django.contrib import admin
from .models import Course, Task


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Show useful course fields in Django Admin for testing and review."""
    list_display = ('name', 'user', 'instructor', 'created_at')
    search_fields = ('name', 'instructor', 'user__username')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Show useful task fields in Django Admin for testing and review."""
    list_display = ('title', 'course', 'priority', 'status', 'due_date')
    list_filter = ('status', 'priority', 'course')
    search_fields = ('title', 'description', 'course__name')
