from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task
from statuses.models import Status
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_('Статус'),
        empty_label=_('не выбрано'),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-400 bg-white rounded-none focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none pr-8 cursor-pointer'
        })
    )
    
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('Исполнитель'),
        required=False,
        empty_label=_('не выбрано'),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-400 bg-white rounded-none focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none pr-8 cursor-pointer'
        })
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Исполнитель'),
        }