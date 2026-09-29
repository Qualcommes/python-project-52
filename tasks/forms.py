from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from statuses.models import Status

from .models import Task

User = get_user_model()

# Единый стиль для стандартных селектов
SELECT_WIDGET_ATTRS = {
    'class': 'w-full px-3 py-2 border border-gray-400 bg-white rounded-none focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none pr-8 cursor-pointer'
}

# Стиль для выпадающего списка с множественным выбором (метки)
MULTISELECT_WIDGET_ATTRS = {
    'class': 'w-full px-3 py-2 border border-gray-400 bg-white rounded-none focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer'
}


class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_('Статус'),
        empty_label=_('не выбрано'),
        widget=forms.Select(attrs=SELECT_WIDGET_ATTRS)
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('Исполнитель'),
        required=False,
        empty_label=_('не выбрано'),
        widget=forms.Select(attrs=SELECT_WIDGET_ATTRS)
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_('Метки'),
        widget=forms.SelectMultiple(attrs=MULTISELECT_WIDGET_ATTRS)
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Исполнитель'),
            'labels': _('Метки'),
        }