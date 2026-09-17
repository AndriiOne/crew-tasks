from django.test import TestCase
from django.urls import reverse

from tasks.models import Position, TaskType, Worker, Task

TASK_URL = reverse("tasks:task-list")
WORKER_URL = reverse("tasks:worker-list")
TASK_TYPE_URL = reverse("tasks:task-type-list")
POSITION_URL = reverse("tasks:position-list")


class TaskDataMixin():
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


class PrivateTasksTests(TaskDataMixin, TestCase):
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


class SearchTasksTests(TestCase):
    def setUp(self):
        self.pos1 = Position.objects.create(
            name="SEO",
        )
        self.pos2 = Position.objects.create(
            name="CEO",
        )
        self.pos3 = Position.objects.create(
            name="PM",
        )
        self.task_type1 = TaskType.objects.create(
            name="type_x",
        )
        self.task_type2 = TaskType.objects.create(
            name="type_y",
        )
        self.task_type3 = TaskType.objects.create(
            name="dance",
        )
        self.user1 = Worker.objects.create_user(
            username="John_Ma",
            first_name="John",
            last_name="Malkovich",
            password="test1234",
            position=self.pos1,
        )
        self.user2 = Worker.objects.create_user(
            username="Adam_Ma",
            first_name="Adam",
            last_name="Malkovich",
            password="test1235",
            position=self.pos2,
        )
        self.user3 = Worker.objects.create_user(
            username="User_Te",
            first_name="User",
            last_name="Tester",
            password="test1236",
            position=self.pos3,
        )
        self.task = Task.objects.create(
            name="TestTask1",
            description="description1",
            task_type=self.task_type1,
            priority=Task.Priority.URGENT,
            deadline="2020-09-30 14:33",
            is_completed=True,
        )
        self.task2 = Task.objects.create(
            name="TestTask2",
            description="description2",
            task_type=self.task_type2,
            priority=Task.Priority.LOW,
            deadline="2020-09-30 14:33",
            is_completed=True,
        )
        self.task3 = Task.objects.create(
            name="NoWay3",
            description="description3",
            task_type=self.task_type3,
            priority=Task.Priority.HIGH,
            deadline="2020-09-30 14:33",
            is_completed=True,
        )
        self.client.force_login(self.user1)

    def test_worker_search(self):
        response = self.client.get(WORKER_URL, {"username": "Ma"})
        result = Worker.objects.filter(username__icontains="Ma")
        self.assertEqual(
            list(response.context["worker_list"]),
            list(result),
        )

    def test_task_search(self):
        response = self.client.get(TASK_URL, {"name": "Test"})
        result = Task.objects.filter(name__icontains="Test")
        self.assertEqual(
            list(response.context["task_list"]),
            list(result),
        )

    def test_position_search(self):
        response = self.client.get(POSITION_URL, {"name": "EO"})
        result = Position.objects.filter(name__icontains="EO")
        self.assertEqual(
            list(response.context["position_list"]),
            list(result),
        )

    def test_task_type_search(self):
        response = self.client.get(TASK_TYPE_URL, {"name": "type"})
        result = TaskType.objects.filter(name__icontains="type")
        self.assertEqual(
            list(response.context["task_types_list"]),
            list(result),
        )

    def test_empty_search(self):
        response = self.client.get(WORKER_URL, {"username": ""})
        self.assertEqual(
            list(response.context["worker_list"]),
            list(Worker.objects.all()),
        )

    def test_empty_search_without_parameters(self):
        response = self.client.get(WORKER_URL)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(Worker.objects.all()),
        )


class ToggleTasksTests(TaskDataMixin, TestCase):
    def test_assign_to_task(self):
        response = self.client.get(
            reverse("tasks:toggle-task-assign", kwargs={"pk": self.task.id})
        )
        self.task.refresh_from_db()
        self.assertTrue(
            self.task.assignees.filter(pk=self.user.id).exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_toggle_status_task(self):
        self.task.is_completed = False
        self.task.save()
        response = self.client.get(
            reverse("tasks:toggle-status-task", kwargs={"pk": self.task.id})
        )
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        self.assertEqual(response.status_code, 302)
