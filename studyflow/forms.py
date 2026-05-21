"""Forms used by StudyFlow views."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Task


class RegisterForm(UserCreationForm):
    """Collect a new user's username, email, and password for registration."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CourseForm(forms.ModelForm):
    """Allow a logged-in user to create or edit one course."""
    class Meta:
        model = Course
        fields = ['name', 'instructor', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


class TaskForm(forms.ModelForm):
    """Allow a logged-in user to create or edit one academic task."""
    class Meta:
        model = Task
        fields = ['course', 'title', 'description', 'due_date', 'priority', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        """Limit the course dropdown so users can only select their own courses."""
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['course'].queryset = Course.objects.filter(user=user)
