from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "urgent", "Urgent"
        HIGH = "high", "High"
        LOW = "low", "Low"

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    is_completed = models.BooleanField(default=False)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(
        Worker, blank=True,
        related_name="assigned_tasks"
    )

    class Meta:
        ordering = ["priority"]

    def __str__(self):
        return self.name
