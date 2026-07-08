from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        TENANT = 'tenant', _('Tenant (Арендатор)')
        LANDLORD = 'landlord', _('Landlord (Арендодатель)')

    # Делаем email уникальным полем для аутентификации
    email = models.EmailField(_('email address'), unique=True)

    # Поле выбора роли
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.TENANT,
        verbose_name=_('Роль пользователя')
    )

    # Настройки для использования email вместо username при авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Django все еще требует username при создании superuser

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def is_landlord(self):
        return self.role == self.Roles.LANDLORD

    @property
    def is_tenant(self):
        return self.role == self.Roles.TENANT