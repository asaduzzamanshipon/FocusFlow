from django.contrib import admin

from .models import (
    Task,
    Routine,
    PomodoroSession,
    Notification,
)


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


@admin.register(PomodoroSession)
class PomodoroSessionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "session_type",
        "duration_minutes",
        "completed_at",
    )

    list_filter = (
        "session_type",
        "completed_at",
    )

    search_fields = (
        "user__username",
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "notification_type",
        "title",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "title",
        "message",
        "user__username",
    )