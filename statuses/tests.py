from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from statuses.models import Status


class StatusTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)

    def test_statuses_list_unauthorized(self):
        response = self.client.get(reverse('statuses_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('statuses_list')}")

    def test_statuses_list_authorized(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/statuses_list.html')
        self.assertContains(response, self.status1.name)

    def test_status_create_view(self):
        self.client.force_login(self.user)
        
        # GET
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)

        # POST Valid
        new_status_data = {'name': 'Новый'}
        response = self.client.post(reverse('status_create'), data=new_status_data)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTrue(Status.objects.filter(name='Новый').exists())

    def test_status_create_duplicate_name(self):
        self.client.force_login(self.user)
        
        # Попытка создать статус с уже существующим именем
        response = self.client.post(
            reverse('status_create'),
            data={'name': self.status1.name}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'name',
            'Статус с таким именем уже существует.'  # изменили 'Именем' на 'именем'
        )

    def test_status_update_view(self):
        self.client.force_login(self.user)
        
        update_url = reverse('status_update', kwargs={'pk': self.status1.pk})
        
        # GET
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)

        # POST Update
        response = self.client.post(update_url, data={'name': 'Завершен'})
        self.assertRedirects(response, reverse('statuses_list'))
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, 'Завершен')

    def test_status_delete_view(self):
        self.client.force_login(self.user)
        
        delete_url = reverse('status_delete', kwargs={'pk': self.status2.pk})
        
        # GET
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

        # POST Delete
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertFalse(Status.objects.filter(pk=self.status2.pk).exists())