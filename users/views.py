from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import ProtectedError

from users.forms import UserRegisterForm, UserUpdateForm


class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    auth_message = _("Вы не авторизованы! Пройдите авторизацию.")
    permission_message = _("У вас нет прав для изменения")
    permission_url = reverse_lazy("users_list")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, self.auth_message)
            return redirect(self.login_url)
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


# 1. Список пользователей (GET /users/)
class UserListView(ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"


# 2. Регистрация (GET/POST /users/create/)
class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("Пользователь успешно зарегистрирован")


# 3. Обновление (GET/POST /users/<int:pk>/update/)
class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users_list")
    success_message = _("Пользователь успешно изменен")


# 4. Удаление (GET/POST /users/<int:pk>/delete/)
class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_list")
    success_message = _("Пользователь успешно удален")
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _('Невозможно удалить пользователя, так как он используется')
            )
            return redirect('users_list') # или ваш URL списка пользователей


# 5. Вход (GET/POST /login/)
class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "users/login.html"
    next_page = reverse_lazy("index")
    success_message = _("Вы залогинены")


# 6. Выход (POST /logout/)
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("Вы разлогинены"))
        return super().dispatch(request, *args, **kwargs)
