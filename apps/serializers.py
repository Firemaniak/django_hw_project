# Создайте эндпоинт для создания новой задачи. Задача должна быть создана
# с полями title, description, status, и deadline.
#
# Шаги для выполнения:
#
# Определите сериализатор для модели Task.
#
# Создайте представление для создания задачи.
#
# Создайте маршрут для обращения к представлению.

from .models import Category, SubTask, Task
from rest_framework import serializers
from django.utils import timezone

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', ]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline',]

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Deadline can`t be in past')
        return value


# Создайте SubTaskCreateSerializer, в котором поле created_at будет доступно только для чтения (read_only).
# Шаги для выполнения:
# Определите SubTaskCreateSerializer в файле serializers.py.
# Переопределите поле created_at как read_only.

class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']


class TaskGetSerializer(serializers.ModelSerializer):
    subtasks = SubTaskCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline',]





# Создайте сериализатор для категории CategoryCreateSerializer, переопределив методы create и update
# для проверки уникальности названия категории. Если категория с таким названием уже существует, возвращайте ошибку валидации.
#
# Шаги для выполнения:
#
# Определите CategoryCreateSerializer в файле serializers.py.
# Переопределите метод create для проверки уникальности названия категории.
# Переопределите метод update для аналогичной проверки при обновлении.

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({'name': 'Category with this name already exists.'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if name and Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'name': 'Category with this name already exists.'})
        return super().update(instance, validated_data)


# Задание 3: Использование вложенных сериализаторов
# Создайте сериализатор для TaskDetailSerializer, который включает вложенный сериализатор для полного отображения
# связанных подзадач (SubTask). Сериализатор должен показывать все подзадачи, связанные с данной задачей.
#
# Шаги для выполнения:
# Определите TaskDetailSerializer в файле serializers.py.
# Вложите SubTaskSerializer внутрь TaskDetailSerializer.




