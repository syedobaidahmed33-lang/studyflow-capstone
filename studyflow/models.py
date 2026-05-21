"""Database models for the StudyFlow task planner."""
from django.conf import settings
from django.db import models


class Course(models.Model):
    """A course belongs to one user and groups related academic tasks together."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=20, default='#2563eb')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Return a readable course name in the admin and templates."""
        return self.name


class Task(models.Model):
    """A task represents one assignment, study goal, or project step for a course."""
    PRIORITY_LOW = 'Low'
    PRIORITY_MEDIUM = 'Medium'
    PRIORITY_HIGH = 'High'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    STATUS_NOT_STARTED = 'Not Started'
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (STATUS_NOT_STARTED, 'Not Started'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NOT_STARTED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date', '-created_at']

    def __str__(self):
        """Return a readable task title in the admin and templates."""
        return self.title

    @property
    def is_completed(self):
        """Provide a simple boolean shortcut for templates and tests."""
        return self.status == self.STATUS_COMPLETED
