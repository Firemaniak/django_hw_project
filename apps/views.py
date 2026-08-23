from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskListSerializer, TaskCreateSerializer, TaskGetSerializer
from .models import Task
from django.db.models import Count
from django.utils import timezone


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
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

