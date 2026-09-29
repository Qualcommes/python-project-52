from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(forms.ModelForm):
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
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput,
        required=True,
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password and len(password) < 3:
            raise ValidationError(
                _("Ваш пароль должен содержать минимум 3 символа.")
            )
        return password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", _("Пароли не совпадают."))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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