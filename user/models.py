from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from passlib.hash import pbkdf2_sha256

from user.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, default='')
    name = models.CharField(max_length=50, blank=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)

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
