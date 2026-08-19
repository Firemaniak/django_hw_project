import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from datetime import timedelta
from django.utils import timezone
from apps.models import SubTask, Task

# Изменение записей:
# Измените статус "Prepare presentation" на "In progress".
# Измените срок выполнения для "Gather information" на два дня назад.
# Измените описание для "Create slides" на "Create and format presentation slides".

now = timezone.now()

update_task = Task.objects.get(title='Prepare presentation')
update_task.status = 'In progress'
update_task.save()

print(f'Для {update_task.title} обновлено поле "Статус" на {update_task.status}')

up_subtask = SubTask.objects.get(title='Gather information')
up_subtask.deadline = now - timedelta(days=2)
up_subtask.save()

print(f'Для {up_subtask.title} был измененон дэдлайна на {up_subtask.deadline}')

up_disc = SubTask.objects.get(title='Create slides')
up_disc.description = 'Create and format presentation slides'
up_disc.save()

print(f'Для {up_disc.title} изменено описание на {up_disc.description}')