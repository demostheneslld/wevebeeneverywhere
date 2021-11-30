"""
Definition of forms.
"""

import uuid
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from blog.models import BlogPost, MediaItem, Profile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user


class SubscribeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']

    def save(self, commit=True):
        user = super(SubscribeForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.is_subscribed_to_emails = True
        if commit:
            user.save()
        return user


class UnsubscribeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']

    def save(self, commit=True):
        email = self.cleaned_data['email']
        user = User.objects.get(email=email)
        user.is_subscribed_to_emails = False
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'greeting', 'default_participants',
                  'map_icon_color', 'is_subscribed_to_emails']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
        }
        labels = {
            'is_subscribed_to_emails': 'Subscribed to Emails?'
        }


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
