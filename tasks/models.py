from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from statuses.models import Status
from labels.models import Label

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Имя'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Статус')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author_tasks',
        verbose_name=_('Автор')
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor_tasks',
        null=True,
        blank=True,
        verbose_name=_('Исполнитель')
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabelRelation',
        blank=True,
        related_name='tasks',
        verbose_name=_('Метки')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        return self.name


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)