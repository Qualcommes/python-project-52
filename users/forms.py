from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("Имя"),
        max_length=150,
        required=True,
    )
    last_name = forms.CharField(
        label=_("Фамилия"),
        max_length=150,
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password and len(password) < 3:
            raise ValidationError(
                _("Ваш пароль должен содержать минимум 3 символа.")
            )
        return password


class UserUpdateForm(UserChangeForm):
    password = None  # Скрываем поле пароля при редактировании личных данных

    first_name = forms.CharField(
        label=_("Имя"),
        max_length=150,
        required=True,
    )
    last_name = forms.CharField(
        label=_("Фамилия"),
        max_length=150,
        required=True,
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")