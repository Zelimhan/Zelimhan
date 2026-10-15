from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'client', 'Клиент'
        REALTOR = 'realtor', 'Риелтор'
        ADMIN = 'admin', 'Админ'

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    phone = models.CharField('Телефон', max_length=32, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_realtor(self):
        return self.role == self.Role.REALTOR

    @property
    def is_site_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
