"""Views for the StudyFlow task planner web application."""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import CourseForm, RegisterForm, TaskForm
from .models import Course, Task


@login_required
def dashboard_view(request):
    """Show the signed-in user's courses, upcoming tasks, and completion progress."""
    status_filter = request.GET.get('status', '')
    tasks = Task.objects.filter(course__user=request.user).select_related('course')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    total_tasks = Task.objects.filter(course__user=request.user).count()
    completed_tasks = Task.objects.filter(course__user=request.user, status=Task.STATUS_COMPLETED).count()
    progress_percent = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

    context = {
        'tasks': tasks,
        'courses': Course.objects.filter(user=request.user),
        'status_filter': status_filter,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress_percent': progress_percent,
        'status_choices': Task.STATUS_CHOICES,
    }
    return render(request, 'studyflow/dashboard.html', context)


def register_view(request):
    """Handle both GET and POST requests for creating a new StudyFlow account."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome to StudyFlow!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'studyflow/register.html', {'form': form})


@login_required
def course_list_view(request):
    """List only the courses owned by the currently signed-in user."""
    courses = Course.objects.filter(user=request.user).prefetch_related('tasks')
    return render(request, 'studyflow/course_list.html', {'courses': courses})


@login_required
def course_create_view(request):
    """Handle GET and POST requests for creating a new course."""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'studyflow/course_form.html', {'form': form, 'heading': 'Add Course'})


@login_required
def task_create_view(request):
    """Handle GET and POST requests for creating a new task connected to a course."""
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'studyflow/task_form.html', {'form': form, 'heading': 'Add Task'})


@login_required
def task_detail_view(request, pk):
    """Display one task if it belongs to the current user."""
    task = get_object_or_404(Task.objects.select_related('course'), pk=pk, course__user=request.user)
    return render(request, 'studyflow/task_detail.html', {'task': task})


@login_required
def task_edit_view(request, pk):
    """Handle GET and POST requests for editing an existing user-owned task."""
    task = get_object_or_404(Task, pk=pk, course__user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'studyflow/task_form.html', {'form': form, 'heading': 'Edit Task'})


@login_required
@require_POST
def task_delete_view(request, pk):
    """Delete one task after confirming it belongs to the current user."""
    task = get_object_or_404(Task, pk=pk, course__user=request.user)
    task.delete()
    messages.info(request, 'Task deleted.')
    return redirect('dashboard')


@login_required
@require_POST
def toggle_task_status_view(request, pk):
    """Toggle a task between completed and in-progress, then return JSON for fetch()."""
    task = get_object_or_404(Task, pk=pk, course__user=request.user)
    if task.status == Task.STATUS_COMPLETED:
        task.status = Task.STATUS_IN_PROGRESS
    else:
        task.status = Task.STATUS_COMPLETED
    task.save()

    total_tasks = Task.objects.filter(course__user=request.user).count()
    completed_tasks = Task.objects.filter(course__user=request.user, status=Task.STATUS_COMPLETED).count()
    progress_percent = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

    return JsonResponse({
        'id': task.pk,
        'status': task.status,
        'completed_count': completed_tasks,
        'total_count': total_tasks,
        'progress_percent': progress_percent,
    })
