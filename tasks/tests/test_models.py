from django.test import TestCase

from tasks.models import Position, TaskType, Worker, Task


class ModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="TestPosition")
        self.task_type = TaskType.objects.create(name="TestTaskType")
        self.task = Task.objects.create(
            name="TestTask",
            description="description",
            task_type=self.task_type,
            priority=Task.Priority.URGENT,
            deadline="2020-09-30 14:33",
            is_completed=True,
        )
        self.worker = Worker.objects.create_user(
            username="TestWorker",
            first_name="TestWorker",
            last_name="TestWorkerL",
            position=self.position,
        )

    def test_position_str(self):
        self.assertEqual(str(self.position), "TestPosition")

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "TestTaskType")

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker),
            f"TestWorker TestWorkerL ({self.position})"
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "TestTask")

    def test_worker_get_absolute_url(self):
        self.assertEqual(
            self.worker.get_absolute_url(),
            f"/workers/{self.worker.id}/",
        )
