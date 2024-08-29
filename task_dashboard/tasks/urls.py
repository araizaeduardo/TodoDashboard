from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('task/new/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/change-state/', views.change_task_state, name='change_task_state'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
]