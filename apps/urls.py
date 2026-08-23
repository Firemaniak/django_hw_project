from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<uuid:pk>/', views.task_id, name='task-id'),
    path('static/', views.task_static, name='task-static'),
    path('create/', views.task_create, name='task-create'),
]