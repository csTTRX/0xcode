from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profil_photo = models.ImageField(verbose_name="photo de profile")
    username = None
    USERNAME_FIELD = "email"