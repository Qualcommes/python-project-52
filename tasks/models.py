from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Имя"),
        error_messages={
            'unique': _("Задача с таким именем уже существует."),
        }
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Описание")
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_("Статус"),
        related_name='tasks'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Автор"),
        related_name='created_tasks'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_("Исполнитель"),
        related_name='assigned_tasks'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )

    def __str__(self):
        return self.name