from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from users import enums


class User(AbstractUser):
    first_name = models.CharField(
        'Имя',
        max_length=enums.UserEnums.FIRST_NAME_MAX_LEN
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=enums.UserEnums.LAST_NAME_MAX_LEN
    )
    username = models.CharField(
        'Логин',
        max_length=enums.UserEnums.USERNAME_MAX_LEN,
        unique=True,
        validators=(
            validators.RegexValidator(
                r'^[\w]+$', 'Логин содержит запрещённый символ!'
            ),
            validators.MinLengthValidator(
                enums.UserEnums.USERNAME_MIN_LEN,
                'Логин слишком короткий'
            ),
        )
    )
    password = models.CharField(
        'Пароль',
        max_length=enums.UserEnums.PASSWORD_MAX_LEN,
        validators=(
            validators.MinLengthValidator(
                enums.UserEnums.PASSWORD_MIN_LEN,
                'Пароль слишком короткий!'
            ),
        )
    )
    email = models.EmailField(
        'Почта',
        max_length=enums.UserEnums.EMAIL_MAX_LEN,
        unique=True,
        validators=(
            validators.EmailValidator('Введите корректный почтовый адрес!'),
        )
    )
    is_active = models.BooleanField('Аккаунт подтверждён', default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='user_unique_subscription_constraint'),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='self_subscription_constraint'),
        )

    def __str__(self):
        return f'{self.author.username} <- {self.user.username}'
