from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="dashboard"),

    path("tasks/", views.tasks, name="tasks"),
    path(
        "tasks/<int:task_id>/complete/",
        views.complete_task,
        name="complete_task"
    ),
    path(
        "tasks/<int:task_id>/delete/",
        views.delete_task,
        name="delete_task"
    ),

    path("routine/", views.routine, name="routine"),
    path(
        "routine/<int:routine_id>/delete/",
        views.delete_routine,
        name="delete_routine"
    ),

    path("pomodoro/", views.pomodoro, name="pomodoro"),
    path("progress/", views.progress, name="progress"),
    path("notifications/", views.notifications, name="notifications"),
]