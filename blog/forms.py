"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from blog.models import BlogPost, MediaItem

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
  email = forms.EmailField(required=True)
  is_subscribed_to_emails = forms.BooleanField(required=False, label='Subscribe to Emails?', initial=False)

  class Meta:
    model = User
    fields = ("username", "password1", "password2", "email", "is_subscribed_to_emails")

  def save(self, commit=True):
    user = super(NewUserForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    user.is_subscribed_to_emails = self.cleaned_data['is_subscribed_to_emails']
    if commit:
      user.save()
    return user

class BlogPostForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'placeholder': 'Select a date',
                'type': 'date'
            }
        ),
    )

    publish_date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_format=('%Y-%m-%d'),
            date_attrs={
                'type': 'date',
                'class': 'mb-1',
            },
            # time_format=('%H:%M %p %Z'),
            time_attrs={
                'type': 'time',
            },
        ),
    )

    content = forms.CharField(
        widget=CKEditorWidget()
    )

    class Meta:
        model = BlogPost
        fields = (
            'title',
            'subtitle',
            'participants',
            'loc_name',
            'lat',
            'lng',
            'event_date',
            'publish_date',
            'score',
            'content',
        )

class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = (
            'media_type',
            'caption',
            'file_name',
            'file_extension',
            'source_url',
            'source_image_file',
        )

class BlogPostFilterForm(forms.Form):
    p_min = forms.DateInput()
    p_max = forms.DateInput()
    h_min = forms.DateInput()
    h_max = forms.DateInput()
    s_min = forms.NumberInput()
    s_max = forms.NumberInput()
    author = forms.TextInput()
    loc = forms.TextInput()
