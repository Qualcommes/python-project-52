from django.test import TestCase
from django.urls import reverse


class TranslationTestCase(TestCase):
    def test_homepage_translations(self):
        # Проверяем русский язык
        response_ru = self.client.get(reverse('index'), HTTP_ACCEPT_LANGUAGE='ru')
        self.assertContains(response_ru, "Менеджер задач")

        # Проверяем английский язык
        response_en = self.client.get(reverse('index'), HTTP_ACCEPT_LANGUAGE='en')
        self.assertContains(response_en, "Task Manager")