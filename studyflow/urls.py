"""Application URL routes for StudyFlow."""
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='studyflow/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('courses/', views.course_list_view, name='course_list'),
    path('courses/new/', views.course_create_view, name='course_create'),
    path('tasks/new/', views.task_create_view, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail_view, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_edit_view, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete_view, name='task_delete'),
    path('api/tasks/<int:pk>/toggle/', views.toggle_task_status_view, name='toggle_task_status'),
]
