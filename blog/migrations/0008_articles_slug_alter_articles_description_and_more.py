# Generated by Django 4.0.2 on 2022-03-02 09:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_sitevisitors'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=250, unique_for_date='post_date'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='articles',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='blogs_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='articles',
            name='outils',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
