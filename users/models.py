from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True, blank=True)
    is_employee = models.BooleanField()
