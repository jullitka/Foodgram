from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import (CASCADE, CharField, EmailField,
                              ForeignKey, Model, UniqueConstraint)


class User(AbstractUser):
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'
    username = CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\z')]
    )
    email = EmailField(
        max_length=254,
        unique=True
    )
    password = CharField(
        max_length=150,
        blank=False
    )
    first_name = CharField(max_length=150)
    last_name = CharField(max_length=150)

    def __str__(self):
        return self.username
    


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
    
