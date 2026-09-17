from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Position, TaskType, Worker, Task

TASK_URL = reverse("tasks:task-list")
WORKER_URL = reverse("tasks:worker-list")
TASK_TYPE_URL = reverse("tasks:task-type-list")
POSITION_URL = reverse("tasks:position-list")


class PublicTasksTests(TestCase):
    def test_task_return_to_anonymous(self):
        res = self.client.get(TASK_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_worker_return_to_anonymous(self):
        res = self.client.get(WORKER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_task_type_return_to_anonymous(self):
        res = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_position_return_to_anonymous(self):
        res = self.client.get(POSITION_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTasksTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="TestPosition")
        self.task_type = TaskType.objects.create(name="TestTaskType")
        self.user = Worker.objects.create_user(
            username="TestUser",
            first_name="TestUser",
            last_name="TestUserL",
            position=self.position,
        )
        self.task = Task.objects.create(
            name="TestTask",
            description="description",
            task_type=self.task_type,
            priority=Task.Priority.URGENT,
            deadline="2020-09-30 14:33",
            is_completed=True,
        )
        self.client.force_login(self.user)

    def test_position_list_opened(self):
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/position_list.html")
        self.assertEqual(
            list(response.context["position_list"]),
            list(Position.objects.all()),
        )

    def test_task_list_opened(self):
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_list.html")
        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.all()),
        )

    def test_task_type_list_opened(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "tasks/task_types_list.html"
        )
        self.assertEqual(
            list(response.context["task_types_list"]),
            list(TaskType.objects.all()),
        )

    def test_worker_list_opened(self):
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_list.html")
        self.assertEqual(
            list(response.context["worker_list"]),
            list(Worker.objects.all()),
        )
