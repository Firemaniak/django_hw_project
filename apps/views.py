from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, filters
from .serializers import TaskListSerializer, TaskCreateSerializer, TaskGetSerializer, SubTaskCreateSerializer, CategoryCreateSerializer
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Category, SubTask, Task
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly



class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return TaskCreateSerializer
        return TaskGetSerializer


@api_view(['GET'])
def task_static(request):
    task_count = Task.objects.count()
    status_task = Task.objects.values('status').annotate(count=Count('id'))
    overdue_task = Task.objects.filter(deadline__lt=timezone.now()).count()

    data = {
        'tast_count': task_count,
        'status_task': list(status_task),
        'overdue_task': overdue_task
    }
    return Response(data, status=status.HTTP_200_OK)



# # @api_view(['GET'])
# # def task_list(request):
# #     tasks = Task.objects.all()
# #     serializer = TaskListSerializer(tasks, many=True)
# #     return Response(serializer.data, status=status.HTTP_200_OK)
#
# WEEKDAY_MAP = {
#     'monday': 2, 'tuesday': 3, 'wednesday': 4, 'thursday': 5,
#     'friday': 6, 'saturday': 7, 'sunday': 1,
#     'понедельник': 2, 'вторник': 3, 'среда': 4, 'четверг': 5,
#     'пятница': 6, 'суббота': 7, 'воскресенье': 1,
# }
#
#
# @api_view(['GET'])
# def task_list(request):
#     weekday_param = request.query_params.get('weekday')
#
#     tasks = Task.objects.all()
#
#     if weekday_param:
#         weekday_number = WEEKDAY_MAP.get(weekday_param.lower())
#         if weekday_number is None:
#             return Response(
#                 {'error': 'Invalid weekday value'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         tasks = tasks.annotate(
#             weekday=ExtractWeekDay('deadline')
#         ).filter(weekday=weekday_number)
#
#     serializer = TaskListSerializer(tasks, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
#
# @api_view(['GET'])
# def task_id(request, pk):
#     try:
#         task = Task.objects.get(pk=pk)
#     except Task.DoesNotExist:
#         return Response({'error': 'Task not found'},
# status=status.HTTP_404_NOT_FOUND)
#     serializer = TaskGetSerializer(task)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
#
# @api_view(['GET'])
# def task_static(request):
#     task_count = Task.objects.count()
#     status_task = Task.objects.values('status').annotate(count=Count('id'))
#     overdue_task = Task.objects.filter(deadline__lt=timezone.now()).count()
#
#     data = {
#         'tast_count' : task_count,
#         'status_task' : list(status_task),
#         'overdue_task' : overdue_task
#     }
#     return Response(data, status=status.HTTP_200_OK)
#
#
#
#
# @api_view(['POST'])
# def task_create(request):
#     serializer = TaskCreateSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




#-----------------------------------------------------------------------------------------------------------------------




class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]



class SubTaskPagination(PageNumberPagination):
    page_size = 5


@api_view(['GET'])
def subtask_list(request):
    subtasks = SubTask.objects.all().order_by('-created_at')
    paginator = SubTaskPagination()
    result_page = paginator.paginate_queryset(subtasks, request)
    serializer = SubTaskCreateSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def subtask_filtered_list(request):
    task_title = request.query_params.get('task_title')
    status_param = request.query_params.get('status')

    subtasks = SubTask.objects.all().order_by('-created_at')

    if task_title:
        subtasks = subtasks.filter(task__title__icontains=task_title)
    if status_param:
        subtasks = subtasks.filter(status=status_param)

    paginator = SubTaskPagination()
    result_page = paginator.paginate_queryset(subtasks, request)
    serializer = SubTaskCreateSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)




# class SubTaskListCreateView(APIView):
#     def get(self, request):
#         subtask = SubTask.objects.all()
#         serializer = SubTaskCreateSerializer(subtask, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,
# status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,
# status=status.HTTP_400_BAD_REQUEST)
#
#
# class SubTaskDetailUpdateDeleteView(APIView):
#     def get(self, request, pk):
#         try:
#             subtask = SubTask.objects.get(pk=pk)
#         except SubTask.DoesNotExist:
#             return Response({'error': 'SubTask not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         serializer = SubTaskCreateSerializer(subtask)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         try:
#             subtask = SubTask.objects.get(pk=pk)
#         except SubTask.DoesNotExist:
#             return Response({'error': 'SubTask not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         serializer = SubTaskCreateSerializer(subtask, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         try:
#             subtask = SubTask.objects.get(pk=pk)
#         except SubTask.DoesNotExist:
#             return Response({'error': 'SubTask not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         subtask.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#
#
#
#
# class SubTaskPagination(PageNumberPagination):
#     page_size = 5
#
#
# @api_view(['GET'])
# def subtask_list(request):
#     subtasks = SubTask.objects.all().order_by('-created_at')
#
#     paginator = SubTaskPagination()
#     result_page = paginator.paginate_queryset(subtasks, request)
#     serializer = SubTaskCreateSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)
#
#
#
#
#
# # views.py
# @api_view(['GET'])
# def subtask_filtered_list(request):
#     task_title = request.query_params.get('task_title')
#     status_param = request.query_params.get('status')
#
#     subtasks = SubTask.objects.all().order_by('-created_at')
#
#     if task_title:
#         subtasks = subtasks.filter(task__title__icontains=task_title)
#
#     if status_param:
#         subtasks = subtasks.filter(status=status_param)
#
#     paginator = SubTaskPagination()
#     result_page = paginator.paginate_queryset(subtasks, request)
#     serializer = SubTaskCreateSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    #permission_classes = [IsAuthenticated]

#Добавьте кастомный метод count_tasks используя декоратор @action для подсчета количества задач, связанных с каждой категорией.
    @action(detail=False, methods = ['Get'])
    def count_tasks(self, request):
        cat_count_tasks = Category.objects.annotate(task_count=Count("tasks"))
        data = [
            {
                "id": category.id,
                "category": category.name,
                "task_count": category.task_count
            }
            for category in cat_count_tasks
        ]
        return Response(data)


# class PrivateView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         return Response({"message": f"Hello, {request.user.username}!"})



#Создайте представления для получения задач текущего пользователя.
#Реализуйте представление для получения задач, принадлежащих текущему пользователю.

class UserTaskListView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)





