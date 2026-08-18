# from django.contrib import admin
# from .models import Task, SubTask, Category
#
# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'categories', 'status', 'deadline', 'created_at')
#
# @admin.register(SubTask)
# class SubTaskAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'task', 'status', 'deadline', 'created_at')
#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)

from django.contrib import admin
from .models import Category, SubTask, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "deadline",
        "created_at",
    )
    list_filter = ("status", "categories")
    search_fields = ("title", "description")
    filter_horizontal = ("categories",)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "task",
        "status",
        "deadline",
        "created_at",
    )
    list_filter = ("status", "task")
    search_fields = ("title", "description")
