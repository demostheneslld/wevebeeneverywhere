# Generated by Django 3.0.7 on 2020-06-10 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='blog_post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateField(default=django.utils.timezone.now)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('participants', models.CharField(max_length=400)),
                ('loc_name', models.CharField(default='Name, CityOrState', max_length=100)),
                ('lat', models.DecimalField(decimal_places=4, max_digits=10)),
                ('lng', models.DecimalField(decimal_places=4, max_digits=10)),
                ('title', models.CharField(max_length=250)),
                ('subtitle', models.CharField(max_length=400)),
                ('content', models.TextField(default='<p>This content must be written in HTML. See the live preview, code shortcuts above, or google for information on syntax.</p>')),
                ('score', models.CharField(choices=[('1', 'Terrible!'), ('2', 'Meh'), ('3', 'Okay'), ('4', 'Good'), ('5', 'Great!'), ('6', 'AMAZING'), ('7', 'All Time Favorite')], default=4, max_length=15)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('greeting', models.TextField(default='Hi', max_length=30)),
                ('default_participants', models.CharField(blank=True, max_length=120)),
                ('map_icon_color', models.CharField(default='red', max_length=40)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='post_interactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('interaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog_post')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
