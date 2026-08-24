from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<uuid:pk>/', views.task_id, name='task-id'),
    path('static/', views.task_static, name='task-static'),
    path('create/', views.task_create, name='task-create'),
    path('subtasks/', views.SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<uuid:pk>/', views.SubTaskDetailUpdateDeleteView.as_view(),name='subtask-detail-update-delete'),
]