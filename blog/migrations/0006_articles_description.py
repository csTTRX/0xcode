# Generated by Django 4.0.2 on 2022-02-23 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_siteinfo_alter_articles_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='description',
            field=models.CharField(default='Un super article qui vous explique etape par etape python', max_length=1200),
            preserve_default=False,
        ),
    ]
