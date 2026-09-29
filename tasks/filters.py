import django_filters
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from statuses.models import Status

from .models import Task

User = get_user_model()

SELECT_WIDGET_ATTRS = {
    'class': 'w-full px-3 py-2 border border-gray-400 bg-white rounded-none focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none pr-8 cursor-pointer'
}


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Статус'),
        empty_label=_('не выбрано'),
        widget=forms.Select(attrs=SELECT_WIDGET_ATTRS)
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Исполнитель'),
        empty_label=_('не выбрано'),
        widget=forms.Select(attrs=SELECT_WIDGET_ATTRS)
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('Метка'),
        empty_label=_('не выбрано'),
        widget=forms.Select(attrs=SELECT_WIDGET_ATTRS)
    )
    self_tasks = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded border-gray-400 text-blue-600 focus:ring-blue-500 h-4 w-4 cursor-pointer'
        })
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настраиваем отображение имени в фильтре
        self.form.fields['executor'].label_from_instance = (
            lambda user: user.get_full_name() or user.username
        )
    
    def filter_self_tasks(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset