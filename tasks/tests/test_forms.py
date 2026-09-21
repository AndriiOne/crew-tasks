from django.test import TestCase

from tasks.forms import WorkerCreationForm, TaskDateForm
from tasks.models import Position, Task, TaskType


class WorkerFormsTests(TestCase):
    def setUp(self):
        position = Position.objects.create(name="Test Position")
        self.form_data = {
            "username": "test",
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@gmail.com",
            "password1": "user12test",
            "password2": "user12test",
            "position": position.id,
        }

    def test_if_worker_creation_have_valid_data(self):
        form_data = self.form_data.copy()
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TaskFormsTests(TestCase):
    def setUp(self):
        task_type = TaskType.objects.create(name="Task Type")
        self.form_data = {
            "name": "Test Task",
            "description": "description",
            "task_type": task_type.id,
            "priority": Task.Priority.URGENT,
            "deadline": "2020-09-30 14:33",
            "is_completed": True,
        }

    def test_if_task_creation_have_valid_data(self):
        form_data = self.form_data.copy()
        form = TaskDateForm(data=form_data)
        self.assertTrue(form.is_valid())
