"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# USER RELATED
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    greeting = models.TextField(max_length=30, default='Hi')
    default_participants = models.CharField(max_length=120, blank=True)
    map_icon_color = models.CharField(max_length=40, default='red')

@receiver(post_save, sender=User)
# pylint: disable=unused-argument
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
# pylint: disable=unused-argument
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# BLOG RELATED
class blog_post(models.Model):
    SCORE_CHOICES = [('1', 'Terrible!'), ('2', 'Meh'), ('3', 'Okay'), ('4', 'Good'), ('5', 'Great!'), ('6', 'AMAZING'), ('7', 'All Time Favorite')]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateField(default=timezone.now)
    publish_date = models.DateTimeField(default=timezone.now)
    participants = models.CharField(max_length=400)
    loc_name = models.CharField(max_length=100, default='Name, CityOrState')
    lat = models.DecimalField(max_digits=10, decimal_places=4)
    lng = models.DecimalField(max_digits=10, decimal_places=4)
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=400)
    content = models.TextField(default='<p>This content must be written in HTML. See the live preview, or google for information on syntax.</p>')
    score = models.CharField(max_length=15, choices=SCORE_CHOICES, default=4)
    def comment_count(self):
        obj_pk = self.id
        return post_interactions.objects.filter(type='comment', post_id=obj_pk).count()
    def like_count(self):
        obj_pk = self.id
        return post_interactions.objects.filter(type='like', post_id=obj_pk).count()
    def get_comments(self):
        obj_pk = self.id
        return post_interactions.objects.filter(type='comment', post_id=obj_pk).order_by('-interaction_date')

# class MediaItem(models.Model):
#     MEDIA_TYPES = [
#         ('1', 'picture'),
#         ('2', 'video')
#     ]
#     media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default=1)
#     title = models.CharField(max_length=250)
#     source_url = models.CharField(max_length=400)
#     content = models.TextField(default='<p>This content must be written in HTML. See the live preview, code shortcuts above, or google for information on syntax.</p>')

class post_interactions(models.Model):
    type = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_id = models.ForeignKey(blog_post, on_delete=models.CASCADE)
    interaction_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
