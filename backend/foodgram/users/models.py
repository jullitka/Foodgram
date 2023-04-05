from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, EmailField,
                              ForeignKey, Model, UniqueConstraint)


class User(AbstractUser):
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'
    email = EmailField(
        max_length=254,
        unique=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Subscription(Model):
    user = ForeignKey(
        User,
        related_name='subscriptions',
        verbose_name='Подписчик',
        on_delete=CASCADE
    )
    author = ForeignKey(
        User,
        related_name='subscribers',
        verbose_name='Подписка',
        on_delete=CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=('author', 'user'), name='subscription')
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
