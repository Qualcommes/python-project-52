from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label=_("Имя"), required=True)
    last_name = forms.CharField(label=_("Фамилия"), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username")


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label=_("Имя"), required=True)
    last_name = forms.CharField(label=_("Фамилия"), required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")