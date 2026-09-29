from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from labels.models import Label
from tasks.models import Task
from statuses.models import Status

User = get_user_model()


class LabelCRUDTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.label1 = Label.objects.get(pk=1)  # Связана с task 1
        self.label2 = Label.objects.get(pk=2)  # Связана с task 2

    # --- Ограничения доступа (Требуется авторизация) ---

    def test_labels_list_requires_login(self):
        response = self.client.get(reverse('labels_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('labels_list')}")

    def test_label_create_requires_login(self):
        response = self.client.get(reverse('label_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('label_create')}")

    # --- CRUD Операции ---

    def test_labels_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label1.name)
        self.assertContains(response, self.label2.name)

    def test_label_create_success(self):
        self.client.force_login(self.user)
        url = reverse('label_create')
        data = {'name': 'срочно'}
        response = self.client.post(url, data, follow=True)

        self.assertRedirects(response, reverse('labels_list'))
        self.assertTrue(Label.objects.filter(name='срочно').exists())
        self.assertContains(response, 'Метка успешно создана')

    def test_label_create_duplicate_name_error(self):
        self.client.force_login(self.user)
        url = reverse('label_create')
        data = {'name': self.label1.name}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        
        # Проверка ошибки в форме через контекст ответа
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)

    def test_label_update_success(self):
        self.client.force_login(self.user)
        url = reverse('label_update', args=[self.label2.id])
        data = {'name': 'критично'}
        response = self.client.post(url, data, follow=True)

        self.assertRedirects(response, reverse('labels_list'))
        self.label2.refresh_from_db()
        self.assertEqual(self.label2.name, 'критично')
        self.assertContains(response, 'Метка успешно изменена')

    def test_label_delete_unused_success(self):
        self.client.force_login(self.user)
        # Создаем метку без связанных задач
        unused_label = Label.objects.create(name='для удаления')
        url = reverse('label_delete', args=[unused_label.id])

        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertFalse(Label.objects.filter(pk=unused_label.id).exists())
        self.assertContains(response, 'Метка успешно удалена')

    def test_label_delete_linked_to_task_fails(self):
        """Защита: Метку, связанную с задачей, удалить нельзя."""
        self.client.force_login(self.user)
        url = reverse('label_delete', args=[self.label1.id])

        # Пытаемся удалить label1 (она привязана к task1)
        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('labels_list'))
        self.assertTrue(Label.objects.filter(pk=self.label1.id).exists())
        self.assertContains(response, 'Невозможно удалить метку')