from django.db import models
from PIL import Image
# Create your models here.

class Project(models.Model):

    name = models.CharField(max_length=120)
    description = models.TextField(max_length=5000)
    image = models.ImageField(verbose_name='project image', upload_to="images/", null = True)
    publish_at = models.DateField(verbose_name='date of publish', null=True, blank=True)
    website = models.URLField(blank=True)
    githup = models.URLField(blank=True)

    IMAGE_MAX_SIZE = (400, 300)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args , **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
        
    def __str__(self):
        return self.name
    
class Formation(models.Model):

    name = models.CharField(max_length=120)
    Level = models.CharField(max_length=120, blank=True, verbose_name="Niveau de formation")
    description = models.TextField(max_length=5000)
    etablisement = models.CharField(max_length=500)
    start_at = models.DateField(verbose_name='Start date ', null=True, blank=True)
    end_at = models.DateField(verbose_name='End date' , null=True, blank=True)
    etab_website = models.URLField(blank=True)

class ExperienceProf(models.Model):

    type = models.CharField(max_length=120)
    description = models.TextField(max_length=5000)
    etablisement = models.CharField(max_length=500)
    poste = models.CharField(max_length=120, blank=True, verbose_name="Niveau de formation")
    start_at = models.DateField(verbose_name='Start date ', null=True, blank=True)
    end_at = models.DateField(verbose_name='End date' , null=True, blank=True)
    etab_website = models.URLField(blank=True)

class Techno(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=5000, blank=True)
    level = models.IntegerField()

class Langue(models.Model):
    name = models.CharField(max_length=120)
    level = models.IntegerField()

class Interet(models.Model):
    name = models.CharField(max_length=120)

class Quality(models.Model):
    name = models.CharField(max_length=120)

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    date = models.DateTimeField(auto_now = True)