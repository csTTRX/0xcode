from django.urls import reverse
from datetime import datetime
from django.db import models
from authentication.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from PIL import Image
class Categories(models.Model):
    name = models.CharField(max_length=200)
    title_tags = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)

    def __str__(self):
        return self.name

class Outils(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    def __str__(self):
        return self.name

class Articles(models.Model):

    title = models.CharField(max_length=200)
    title_tags = models.CharField(blank = True, null = True, max_length=200)
    slug = models.SlugField(max_length=250, default='',editable=False,)
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    body = RichTextUploadingField()
    post_date = models.DateTimeField(auto_created=True)
    update_date = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    outils = models.CharField(max_length=500, blank=True, null=True)
    likes = models.ManyToManyField(User ,related_name='blogs_likes', blank=True, null=True)
    description = models.TextField()

    class Meta:
        ordering = ['update_date']
        permissions = [
            ("premium_articles", "Peut voir les articles premiums" )
        ]

    def __str__(self):
        return str(self.user)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("show_article", args=[self.slug])
    
    def save(self,*args, **kwargs):
        self.slug = slugify('-'.join([self.title, 
            str(self.post_date.year),
            str(self.post_date.month)]),
            allow_unicode=False)
        super(Articles, self).save(*args, **kwargs)
    
class Comments(models.Model):

    article = models.ForeignKey(Articles,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
    

class SiteInfo(models.Model):
    title = models.CharField(max_length=200)
    title_tags = models.CharField(max_length=200)
    body = RichTextUploadingField()

    def __str__(self):
        return self.title
    
class SiteVisitors(models.Model):
    ip_address = models.GenericIPAddressField()
    page_visited = models.TextField()
    event_date = models.DateTimeField(default=datetime.now)