from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password

from user.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True, blank=False)
    first_name = models.CharField(_('Nome'), max_length=150, blank=False)
    last_name = models.CharField(_('Sobrenome'), max_length=150, blank=False)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class Phone(models.Model):
    number = models.IntegerField()
    area_code = models.IntegerField()
    country_code = models.CharField(max_length=5)
    user = models.ForeignKey(
        User, related_name='phones', on_delete=models.CASCADE, blank=False,
        null=False
    )

    def __str__(self):
        return self.number
