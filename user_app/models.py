import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.template.loader import render_to_string


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

        user.is_staff = user.is_superuser = True
        user.save(using=self._db)

        return user

    def has_superuser(self):
        return User.objects.filter(is_superuser=True).count() > 0


class User(AbstractBaseUser, PermissionsMixin):
    # Mocked path to user avatar photo
    avatar_url = models.URLField(null=True, blank=True, default='https://randomuser.me/api/portraits/lego/5.jpg')

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

    achievements = models.ManyToManyField('Achievement', through='AcquiredAchievement', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return str(self.email)


class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.TextField(null=False, blank=False)

    icon_class = models.TextField(null=False, blank=False, validators=[
        RegexValidator(
            regex=r'^(fas|far|fal|fab|fad|) fa-[-\w]+$',
            message='Invalid font-awesom icon class',
            code='invalid_icon_class'
        )
    ])

    color = models.CharField(null=False, blank=False, default='ffffff', max_length=6, validators=[
        RegexValidator(
            regex='^[0-9a-f]{6}$',
            message='Provide color as six hexadecimal digits.',
            code='invalid_color'
        ),
    ])

    def __str__(self):
        return f"Achievement | {self.title}"

    @classmethod
    def _text_color(cls, bg_color: str) -> str:
        if len(bg_color) == 6:
            red, green, blue = [int(bg_color[i:i+2], 16) for i in range(0, 6, 2)]

            # NOTE: based on: https://stackoverflow.com/a/3943023/5822988
            if (red*0.299 + green*0.587 + blue*0.114) <= 186:
                return 'ffffff'

        return '000000'

    @property
    def text_color(self):
        return self._text_color(self.color)

    def to_html(self):
        return render_to_string("user_app/_achievement.html", {'achievement': self}, None)


class AcquiredAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    achievement = models.ForeignKey(Achievement,  on_delete=models.CASCADE, null=False)

    acquired_at = models.DateTimeField(auto_now_add=True, null=False, blank=False, editable=False)

    class Meta:
        auto_created = True  # HACK: otherwise django rise some integrity errors and prevent of using horizontal_filter in admin
        unique_together = ('user', 'achievement')
