from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True,
        null=True
    )

    due_date = models.DateField()

    due_time = models.TimeField(
        blank=True,
        null=True
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["due_time", "created_at"]

    def __str__(self):
        return self.title


class Routine(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="routines"
    )

    title = models.CharField(max_length=200)

    subject = models.CharField(
        max_length=150,
        blank=True
    )

    start_time = models.TimeField()

    end_time = models.TimeField(
        blank=True,
        null=True
    )

    day = models.CharField(
        max_length=20,
        default="Everyday"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return self.title