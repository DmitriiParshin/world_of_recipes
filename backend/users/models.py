from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

from api.validators import username_validator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=settings.LIMIT_EMAIL,
        unique=True,
        error_messages={
            "unique": "Пользователь с такой почтой уже существует!",
        },
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        validators=(username_validator,),
        error_messages={
            "unique": "Пользователь с таким именем уже существует!",
        },
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=settings.LIMIT_USERNAME,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=settings.LIMIT_USERNAME,
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=settings.LIMIT_USERNAME,
    )
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-id",)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username="me"), name="name_not_me"
            )
        ]

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name="follower",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="following",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("author", "user")
        constraints = [
            models.UniqueConstraint(
                fields=("author", "user"),
                name="Подписка уже существует!",
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F("user")),
                name="Подписка на самого себя не разрешена.",
            ),
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
