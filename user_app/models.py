from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, display_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not display_name:
            raise ValueError('Users must have a display name')

        user = self.model(
            email=email,
            display_name=display_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, display_name, password=None):
        user = self.create_user(email, display_name, password=password)

        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    display_name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return str(self.email)
