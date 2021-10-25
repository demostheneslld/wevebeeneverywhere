"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from blog.models import blog_post

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

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = blog_post
        fields = ('event_date', 'participants', 'loc_name', 'lat', 'lng', 'title', 'subtitle', 'score', 'content', 'publish_date'
                  )
        widgets = {
            'event_date': forms.DateInput(), 'publish_date': forms.DateTimeInput(), 'subtitle': forms.Textarea(attrs={'rows': 2, 'cols': 180}), 'content': forms.Textarea(attrs={'rows': 15, 'cols': 180})
        }

class BlogPostFilterForm(forms.Form):
    p_min = forms.DateInput()
    p_max = forms.DateInput()
    h_min = forms.DateInput()
    h_max = forms.DateInput()
    s_min = forms.NumberInput()
    s_max = forms.NumberInput()
    author = forms.TextInput()
    loc = forms.TextInput()
