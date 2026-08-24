from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskListSerializer, TaskCreateSerializer, TaskGetSerializer, SubTaskCreateSerializer
from .models import Task, SubTask
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
from rest_framework.pagination import PageNumberPagination



# @api_view(['GET'])
# def task_list(request):
#     tasks = Task.objects.all()
#     serializer = TaskListSerializer(tasks, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

WEEKDAY_MAP = {
    'monday': 2, 'tuesday': 3, 'wednesday': 4, 'thursday': 5,
    'friday': 6, 'saturday': 7, 'sunday': 1,
    'понедельник': 2, 'вторник': 3, 'среда': 4, 'четверг': 5,
    'пятница': 6, 'суббота': 7, 'воскресенье': 1,
}


@api_view(['GET'])
def task_list(request):
    weekday_param = request.query_params.get('weekday')

    tasks = Task.objects.all()

    if weekday_param:
        weekday_number = WEEKDAY_MAP.get(weekday_param.lower())
        if weekday_number is None:
            return Response(
                {'error': 'Invalid weekday value'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tasks = tasks.annotate(
            weekday=ExtractWeekDay('deadline')
        ).filter(weekday=weekday_number)

    serializer = TaskListSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def task_id(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'},
status=status.HTTP_404_NOT_FOUND)
    serializer = TaskGetSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def task_static(request):
    task_count = Task.objects.count()
    status_task = Task.objects.values('status').annotate(count=Count('id'))
    overdue_task = Task.objects.filter(deadline__lt=timezone.now()).count()

    data = {
        'tast_count' : task_count,
        'status_task' : list(status_task),
        'overdue_task' : overdue_task
    }
    return Response(data, status=status.HTTP_200_OK)




@api_view(['POST'])
def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# Создание классов представлений
# Создайте классы представлений для работы с подзадачами (SubTasks), включая создание, получение, обновление
# и удаление подзадач. Используйте классы представлений (APIView) для реализации этого функционала.
#
# Шаги для выполнения:
# Создайте классы представлений для создания и получения списка подзадач (SubTaskListCreateView).
# Создайте классы представлений для получения, обновления и удаления подзадач (SubTaskDetailUpdateDeleteView).

class SubTaskListCreateView(APIView):
    def get(self, request):
        subtask = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtask, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'SubTask not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'SubTask not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'SubTask not found'},
                            status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






class SubTaskPagination(PageNumberPagination):
    page_size = 5


@api_view(['GET'])
def subtask_list(request):
    subtasks = SubTask.objects.all().order_by('-created_at')

    paginator = SubTaskPagination()
    result_page = paginator.paginate_queryset(subtasks, request)
    serializer = SubTaskCreateSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)





# views.py
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


