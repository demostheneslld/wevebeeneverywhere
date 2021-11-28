# Generated by Django 3.2.8 on 2021-11-28 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_mediaitem_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_subscribed_to_emails',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='file_extension',
            field=models.CharField(choices=[('jpg', 'png'), ('png', 'jpg'), ('png', 'jpeg')], default=1, max_length=10),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='media_type',
            field=models.CharField(choices=[('picture', 'picture'), ('video', 'video')], default=1, max_length=10),
        ),
    ]
