
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task
from statuses.models import Status

User = get_user_model()


class TaskTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.author = User.objects.get(pk=1)
        self.other_user = User.objects.get(pk=2)
        self.status = Status.objects.get(pk=1)
        self.task1 = Task.objects.get(pk=1)

        # Статичные URL-маршруты согласно ТЗ
        self.list_url = reverse('task_list') if self._has_url('task_list') else '/tasks/'
        self.create_url = reverse('task_create') if self._has_url('task_create') else '/tasks/create/'
        self.detail_url = reverse('task_detail', args=[self.task1.id]) if self._has_url('task_detail') else f'/tasks/{self.task1.id}/'
        self.update_url = reverse('task_update', args=[self.task1.id]) if self._has_url('task_update') else f'/tasks/{self.task1.id}/update/'
        self.delete_url = reverse('task_delete', args=[self.task1.id]) if self._has_url('task_delete') else f'/tasks/{self.task1.id}/delete/'

    def _has_url(self, name):
        try:
            reverse(name, args=[1] if name in ['task_detail', 'task_update', 'task_delete'] else [])
            return True
        except Exception:
            return False

    def test_anonymous_redirect(self):
        """Анонимный пользователь должен перенаправляться на страницу входа."""
        response = self.client.get(self.list_url)
        self.assertRedirects(response, f'/login/?next={self.list_url}')

    def test_task_list(self):
        """Авторизованный пользователь видит список задач."""
        self.client.force_login(self.author)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)

    def test_task_detail(self):
        """Просмотр детальной страницы задачи."""
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task1.description)

    def test_create_task(self):
        """Создание задачи (автор проставляется автоматически)."""
        self.client.force_login(self.author)
        data = {
            'name': 'Новая уникальная задача',
            'description': 'Описание новой задачи',
            'status': self.status.id,
            'executor': self.other_user.id,
        }
        response = self.client.post(self.create_url, data)
        self.assertRedirects(response, self.list_url)

        new_task = Task.objects.get(name='Новая уникальная задача')
        self.assertEqual(new_task.author, self.author)
        self.assertEqual(new_task.executor, self.other_user)

    def test_update_task(self):
        """Редактирование задачи."""
        self.client.force_login(self.author)
        data = {
            'name': 'Обновленное имя задачи',
            'description': 'Обновленное описание',
            'status': self.status.id,
            'executor': self.author.id,
        }
        response = self.client.post(self.update_url, data)
        self.assertRedirects(response, self.list_url)

        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, 'Обновленное имя задачи')

    def test_delete_task_by_author(self):
        """Автор может успешно удалить свою задачу."""
        self.client.force_login(self.author)
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Task.objects.filter(pk=self.task1.id).exists())

    def test_delete_task_by_non_author(self):
        """Не-автор НЕ может удалить чужую задачу."""
        self.client.force_login(self.other_user)
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Task.objects.filter(pk=self.task1.id).exists())

    def test_user_cannot_be_deleted_if_has_tasks(self):
        """Пользователя нельзя удалить, если он связан с задачами."""
        self.client.force_login(self.author)
        delete_user_url = f'/users/{self.author.id}/delete/'
        response = self.client.post(delete_user_url)
        self.assertTrue(User.objects.filter(pk=self.author.id).exists())