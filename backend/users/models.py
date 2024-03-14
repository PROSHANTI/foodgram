from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

import foodgram.constants as const


class User(AbstractUser):
    email = models.EmailField(
        max_length=const.MAX_LENGTH_EMAIL,
        unique=True,
        null = False,
        verbose_name="Адрес электронной почты",
    )
    username = models.CharField(
        max_length=const.MAX_LENGTH_USERNAME,
        unique=True,
        null = False,
        verbose_name="Уникальный юзернейм",
        validators=[RegexValidator(
            r'^[\w.@+-]+\Z', message='Введите правильный юзернейм.'
        )],
    )
    first_name = models.CharField(
        max_length=const.MAX_LENGTH_FIRST_NAME,
        null = False,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=const.MAX_LENGTH_LAST_NAME,
        null = False,
        verbose_name="Фамилия",
    )
    password = models.CharField(
        max_length=const.MAX_LENGTH_PASSWORD,
        verbose_name="Пароль",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"{self.username}: {self.email}"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]
