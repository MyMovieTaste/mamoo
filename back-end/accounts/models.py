from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """유저 클래스"""
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
