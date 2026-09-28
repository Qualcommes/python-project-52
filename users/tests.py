from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UsersCRUDTestCase(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.new_user_data = {
            "username": "new_user",
            "first_name": "Alex",
            "last_name": "Rover",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        }

    def test_users_list_view(self):
        """Список пользователей доступен без авторизации."""
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

    def test_user_registration(self):
        """Регистрация создает пользователя и редиректит на страницу входа."""
        response = self.client.post(reverse("user_create"), data=self.new_user_data)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="new_user").exists())

    def test_user_login_and_logout(self):
        """Проверка успешного входа и выхода из системы."""
        # Устанавливаем пароль для проверки аутентификации
        self.user1.set_password("password123")
        self.user1.save()

        # Логин
        login_response = self.client.post(
            reverse("login"),
            data={"username": "john_doe", "password": "password123"},
        )
        self.assertRedirects(login_response, reverse("index"))

        # Логаут
        logout_response = self.client.post(reverse("logout"))
        self.assertRedirects(logout_response, reverse("index"))

    def test_user_update_self(self):
        """Пользователь может редактировать только свою учетную запись."""
        self.client.force_login(self.user1)

        update_url = reverse("user_update", kwargs={"pk": self.user1.pk})
        updated_data = {
            "username": "john_updated",
            "first_name": "Johnathan",
            "last_name": "Doe",
        }

        response = self.client.post(update_url, data=updated_data)
        self.assertRedirects(response, reverse("users_list"))

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "john_updated")
        self.assertEqual(self.user1.first_name, "Johnathan")

    def test_user_update_another_user_denied(self):
        """Попытка изменить чужой профиль приводит к ошибке доступа."""
        self.client.force_login(self.user1)

        update_url = reverse("user_update", kwargs={"pk": self.user2.pk})
        updated_data = {
            "username": "hacked_user",
            "first_name": "Hacked",
            "last_name": "User",
        }

        response = self.client.post(update_url, data=updated_data)
        self.assertRedirects(response, reverse("users_list"))

        self.user2.refresh_from_db()
        self.assertNotEqual(self.user2.username, "hacked_user")

    def test_user_delete_self(self):
        """Пользователь может удалить свой аккаунт."""
        self.client.force_login(self.user1)

        delete_url = reverse("user_delete", kwargs={"pk": self.user1.pk})
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse("users_list"))
        self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())

    def test_user_delete_another_user_denied(self):
        """Пользователь не может удалить чужой аккаунт."""
        self.client.force_login(self.user1)

        delete_url = reverse("user_delete", kwargs={"pk": self.user2.pk})
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse("users_list"))
        self.assertTrue(User.objects.filter(pk=self.user2.pk).exists())