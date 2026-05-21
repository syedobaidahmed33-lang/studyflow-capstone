"""Basic tests for the StudyFlow capstone project."""
from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Course, Task


class StudyFlowModelTests(TestCase):
    """Test that StudyFlow models store course and task data correctly."""
    def test_task_belongs_to_course_and_user(self):
        user = User.objects.create_user(username='student', password='Testpass123')
        course = Course.objects.create(user=user, name='IT 140')
        task = Task.objects.create(course=course, title='Finish capstone', due_date=date.today())
        self.assertEqual(task.course.user.username, 'student')
        self.assertFalse(task.is_completed)


class StudyFlowViewTests(TestCase):
    """Test important authenticated views and the JSON toggle endpoint."""
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='Testpass123')
        self.course = Course.objects.create(user=self.user, name='IT 140')
        self.task = Task.objects.create(course=self.course, title='Study Django', due_date=date.today())

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_toggle_task_status_returns_json(self):
        self.client.login(username='student', password='Testpass123')
        response = self.client.post(reverse('toggle_task_status', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], Task.STATUS_COMPLETED)
