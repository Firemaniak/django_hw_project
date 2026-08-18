from django.db import models


STATUS_CHOICES = [
    ("new", "New"),
    ("in_progress", "In progress"),
    ("pending", "Pending"),
    ("blocked", "Blocked"),
    ("done", "Done"),
]


class Category(models.Model):
    name = models.CharField(max_length=100) #unique=True)

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')
        ]

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(
        Category,
        related_name="tasks",
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_task'
        ordering = ('-created_at',)
        verbose_name = 'Task'
        constraints = [
            models.UniqueConstraint(
                fields=["title", "deadline"],
                name="unique_task_title_deadline",
            )
        ]

    def __str__(self):
        return self.title


# Добавьте несколько объектов для каждой модели.
#
# Оформите ответ:
#
# Прикрепите ссылку на гит и скриншоты, где видны созданные объекты к ответу на домашнее задание.



class SubTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ('-created_at',)
        verbose_name = 'SubTask'
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_subtask_title')
        ]

    def __str__(self):
        return self.title


