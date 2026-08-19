import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from datetime import timedelta
from django.utils import timezone
from apps.models import SubTask, Task

#----------------------------------------------------
SubTask.objects.all().delete()
Task.objects.all().delete()
#----------------------------------------------------

now = timezone.now()

new_task = Task.objects.create(
title="Prepare presentation",
description="Prepare materials and slides for the presentation",
status="New",
deadline= now + timedelta(days=3)
)
print(new_task.id)


new_subtasks = [
    SubTask(title="Gather information", description="Find necessary information for the presentation",
            status="New", deadline=now + timedelta(days=2), task=new_task),
    SubTask(title="Create slides", description="Create presentation slides", status="New",
            deadline=now + timedelta(days=1), task=new_task),
]

SubTask.objects.bulk_create(new_subtasks)








