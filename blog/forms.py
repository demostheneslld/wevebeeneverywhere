"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from blog.models import BlogPost, MediaItem

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))


# widgets = {
#             'event_date': forms.DateInput(),
#             'publish_date': forms.DateTimeInput(),
#             'subtitle': forms.Textarea(attrs={'rows': 2, 'cols': 180}),
#             'content': forms.Textarea(attrs={'rows': 15, 'cols': 180}),
#         }

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
            #time_format=('%H:%M %p %Z'),
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
