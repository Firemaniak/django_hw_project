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


class SubTaskInline(admin.TabularInline):  # или StackedInline, если нужно подробнее
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "short_title",
        "status",
        "deadline",
        "created_at",
    )
    list_filter = ("status", "categories")
    search_fields = ("title", "description")
    filter_horizontal = ("categories",)

    inlines = [SubTaskInline]

    def short_title(self,obj):
        if len(obj.title) > 10:
            return f'{obj.title[:10]}...'
        return obj.title

    short_title.short_description = "Title"


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

    actions = ["mark_as_done"]

    def mark_as_done(self, request, queryset):
        queryset.update(status="done")

    mark_as_done.short_description = "Замена статуса в подзадачи на Done"