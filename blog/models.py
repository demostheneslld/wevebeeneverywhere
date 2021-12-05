"""
Definition of models.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# USER RELATED

from django.contrib.auth.models import User

from blog.email_helper import send_email
User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    greeting = models.CharField(max_length=30, default='Hi')
    default_participants = models.CharField(max_length=120, blank=True)
    map_icon_color = models.CharField(max_length=40, default='red')
    is_subscribed_to_emails = models.BooleanField(default=False)


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


class BlogPost(models.Model):
    SCORE_CHOICES = [('1', 'Terrible!'), ('2', 'Meh'), ('3', 'Okay'), ('4', 'Good'),
                     ('5', 'Great!'), ('6', 'AMAZING'), ('7', 'All Time Favorite')]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateField(default=timezone.now)
    publish_date = models.DateTimeField(default=None, blank=True, null=True)
    email_sent = models.BooleanField(default=False)
    participants = models.CharField(max_length=400, blank=True, null=True)
    loc_name = models.CharField(max_length=100, default='Name, CityOrState')
    lat = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    lng = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    subtitle = models.CharField(max_length=400, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    score = models.CharField(
        max_length=15, choices=SCORE_CHOICES, default=4, null=True)

    def strict_validate(self):
        errors = []
        if not self.participants:
            errors.append('Participants is required')
        if not self.loc_name:
            errors.append('Location Name is required')
        if not self.title:
            errors.append('Title is required')
        if not self.subtitle:
            errors.append('Subtitle is required')
        if not self.content:
            errors.append('You must write something in the post content')
        return errors

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def unpublish(self):
        self.publish_date = None
        self.save()

    def send_email(self):
        subscribed_users = Profile.objects.filter(is_subscribed_to_emails=True)
        subject = f'''New Post: {self.title}!'''
        body = f'''
<p>We have a new story!<br/>
Check it out :)</p>
<p>
  <b>{self.title}</b><br/>
  <i>{self.subtitle}</i><br/>
  <a href='https://wevebeeneverywhere.com/stories?id={self.id}'>Click here to read the story!</a>
</p>
<p>Thanks for reading,<br/>
Nathan and Molly</p>
<p>Want to change how you receive these emails?<br/>
You can <a href='https://wevebeeneverywhere.com/accounts/profile'>update your preferences</a> or <a href='https://wevebeeneverywhere.com/accounts/unsubscribe'>unsubscribe from this list</a>.</p>
'''
        for subscribed_user in subscribed_users:
            recipient = subscribed_user.user.email
            print('Sending email to ' + recipient)
            send_email(recipient, subject, body)
        self.email_sent = True
        self.save()
        return len(subscribed_users)

    def comment_count(self):
        obj_pk = self.id
        return PostInteraction.objects.filter(type='comment', post_id=obj_pk).count()

    def like_count(self):
        obj_pk = self.id
        return PostInteraction.objects.filter(type='like', post_id=obj_pk).count()

    def get_comments(self):
        obj_pk = self.id
        return PostInteraction.objects.filter(type='comment', post_id=obj_pk).order_by('-interaction_date')


class MediaItem(models.Model):
    MEDIA_TYPES = [
        ('picture', 'picture'),
        ('video', 'video')
    ]
    ALLOWED_FILE_EXTENSIONS = [
        ('jpg', 'png'),
        ('png', 'jpg'),
        ('png', 'jpeg'),
    ]
    post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    media_type = models.CharField(
        max_length=10, choices=MEDIA_TYPES, default=1)
    caption = models.CharField(max_length=250)
    file_name = models.UUIDField()
    file_extension = models.CharField(
        max_length=10, choices=ALLOWED_FILE_EXTENSIONS, default=1)
    source_url = models.CharField(max_length=400)
    source_image_file = models.ImageField(upload_to='post_uploads')


class PostInteraction(models.Model):
    type = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    interaction_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
