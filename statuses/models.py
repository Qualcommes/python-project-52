from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Имя"),
        error_messages={
            'unique': _("Статус с таким именем уже существует."),
        }
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )

    def __str__(self):
        return self.name