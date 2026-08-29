# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('tasks/', views.task_list, name='task-list'),
#     path('tasks/<uuid:pk>/', views.task_id, name='task-id'),
#     path('static/', views.task_static, name='task-static'),
#     path('create/', views.task_create, name='task-create'),
#     path('subtasks/', views.SubTaskListCreateView.as_view(), name='subtask-list-create'),
#     path('subtasks/<uuid:pk>/', views.SubTaskDetailUpdateDeleteView.as_view(),name='subtask-detail-update-delete'),
#     path('tasks/', views.task_list, name='task-list'),
#     path('subtasks/', views.subtask_list, name='subtask-list'),
#     path('subtasks/filter/', views.subtask_filtered_list, name='subtask-filtered-list'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskListCreateView, TaskDetailUpdateDeleteView, task_static,
    SubTaskListCreateView, SubTaskDetailUpdateDeleteView, UserTaskListView,
    subtask_list, subtask_filtered_list, CategoryViewSet
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'catigories', CategoryViewSet)

urlpatterns = [
    path('tasks/my/', UserTaskListView.as_view(), name='user-task-list'),
    path('tasks/stats/', task_static, name='task-stats'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<uuid:pk>/', TaskDetailUpdateDeleteView.as_view(), name='task-detail-update-delete'),

    path('subtasks/paginated/', subtask_list, name='subtask-paginated'),
    path('subtasks/filtered/', subtask_filtered_list, name='subtask-filtered'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<uuid:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),

    path('', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]