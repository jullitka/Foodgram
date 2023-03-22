from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']
    email = models.EmailField()
    password = models.CharField(
        max_length=150,
        blank=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
