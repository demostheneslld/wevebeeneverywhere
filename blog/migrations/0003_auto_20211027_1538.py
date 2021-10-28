# Generated by Django 3.2.8 on 2021-10-27 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_mediaitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MediaItem',
        ),
        migrations.AlterField(
            model_name='blog_post',
            name='content',
            field=models.TextField(default='<p>This content must be written in HTML. See the live preview, or google for information on syntax.</p>'),
        ),
    ]