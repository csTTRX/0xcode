from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth.models import AbstractUser,Group, BaseUserManager
from django.conf import settings
from django.contrib.auth import get_user_model
from PIL import Image

class User(AbstractUser):

    CREATOR = "CREATOR"
    SUBSCRIBER = "SUBSCRIBER"

    ROLE_CHOICE = (

        (CREATOR, 'Createur'),
        (SUBSCRIBER, 'Abonné')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICE, default=SUBSCRIBER, verbose_name="role", blank=True)
    can_post = models.BooleanField(default=False , blank=True)
    is_premium = models.BooleanField(default=False)

    follows = models.ManyToManyField(
        'self',
        limit_choices_to={'role':CREATOR},
        symmetrical=False,
        verbose_name= "suit",
        blank=True,
    )

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_premium:
            group = Group.objects.get(name = 'premiums')
            group.user_set.add(self)

        if self.role == self.CREATOR:
            if self.can_post:
                group = Group.objects.get(name = 'creators')
                group.user_set.add(self)
            else:
                group = Group.objects.get(name = 'subscribers')
                group.user_set.add(self)
        elif self.role==self.SUBSCRIBER:
            group = Group.objects.get(name = 'subscribers')
            group.user_set.add(self)


    def __str__(self):

        if self.username:
            return self.username
        
        elif self.first_name and self.last_name:
            return self.first_name + "  " + self.last_name
        else:
            return self.email
    

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(verbose_name="photo de profile", null= True)
    biograph = models.TextField(blank=True, null= True, verbose_name='qui êtes vous')
    facebook_url = models.CharField(max_length=255, blank=True, null= True)
    twitter_url = models.CharField(max_length=255, blank=True, null= True)
    instagram_url = models.CharField(max_length=255, blank=True, null= True)
    linkedin_url = models.CharField(max_length=255, blank=True, null= True)
    github_url = models.CharField(max_length=255, blank=True, null= True)

    IMAGE_MAX_SIZE = (300, 300)

    def resize_image(self):
        photo = Image.open(self.photo)
        photo.thumbnail(self.IMAGE_MAX_SIZE)
        photo.save(self.photo.path)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
    def __str__(self):
        return str(self.user)
    