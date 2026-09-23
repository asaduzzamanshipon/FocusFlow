from django.contrib import admin
from .models import Task, Routine


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "due_date",
        "due_time",
        "completed",
    )

    list_filter = (
        "completed",
        "due_date",
    )

    search_fields = (
        "title",
        "user__username",
    )


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "user",
        "start_time",
        "end_time",
        "day",
    )

    list_filter = (
        "day",
    )

    search_fields = (
        "title",
        "subject",
        "user__username",
    )