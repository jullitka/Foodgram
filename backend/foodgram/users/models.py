from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\z')]
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    password = models.CharField(
        max_length=150,
        blank=False
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriptions',
        verbose_name='Подписчик',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        verbose_name='Подписка',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'author')

    def __str__(self):
        return self.author
    
