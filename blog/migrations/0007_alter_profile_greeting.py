# Generated by Django 3.2.8 on 2021-11-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20211128_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='greeting',
            field=models.CharField(default='Hi', max_length=30),
        ),
    ]
