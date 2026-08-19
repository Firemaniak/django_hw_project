import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from datetime import timedelta
from django.utils import timezone
from apps.models import SubTask, Task


# Tasks со статусом "New":
# Вывести все задачи, у которых статус "New".

now = timezone.now()

new_tasks = Task.objects.filter(status='New')
print('Задачи со статусом New:')
for task in new_tasks:
    print(f'-{task.title}')

# SubTasks с просроченным статусом "Done":

old_subtasks = SubTask.objects.filter(status='Done', deadline__lt=now)
print('Подзадачи с просроченным статусом Done:')
for st in old_subtasks:
    print(f'-{st.title}')
