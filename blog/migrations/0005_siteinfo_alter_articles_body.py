# Generated by Django 4.0.2 on 2022-02-15 16:24

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_comments_options_remove_articles_photo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('title_tags', models.CharField(max_length=200)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
        ),
        migrations.AlterField(
            model_name='articles',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='an article'),
            preserve_default=False,
        ),
    ]
