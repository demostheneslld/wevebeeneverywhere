"""wbe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

Definition of urls for wbe.
"""

from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

import blog.forms
import blog.views

# Uncomment the next lines to enable the admin:

admin.autodiscover()

urlpatterns = [
    # Public Access
    url(r'^$', blog.views.home, name='home'),
    url(r'^contact$', blog.views.contact, name='contact'),
    url(r'^map$', blog.views.travel_map, name='map'),
    url(r'^sitemap$', blog.views.sitemap, name='sitemap'),
    url(r'^stories$', blog.views.stories, name='stories'),
    url(r'^storyfinder$', blog.views.storyfinder, name='storyfinder'),
    url(r'^action$', blog.views.action, name='action'),
    url(r'^privacy$', blog.views.privacy, name='privacy'),
    url(r'^terms', blog.views.terms, name='terms'),

    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/register", blog.views.register, name="register"),

    # Administration
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),

    # Manage Posts
    url(r'^manage/blog_post/$', blog.views.manage_blog_post_list,
        name='manage_blog_post_list'),
    url(r'^manage/blog_post/(?P<pk>\d+)/change/$',
        blog.views.manage_blog_post_change, name='manage_blog_post_change'),
    url(r'^manage/blog_post/(?P<pk>\d+)/upload_image/$',
        blog.views.manage_blog_post_upload_image, name='manage_blog_post_upload_image'),
    url(r'^manage/blog_post/add/$', blog.views.manage_blog_post_add,
        name='manage_blog_post_add'),
    url(r'^manage/blog_post/(?P<pk>\d+)/delete/$',
        blog.views.manage_blog_post_delete, name='manage_blog_post_delete'),
    url(r'^manage/download_database',
        blog.views.download_database, name='download_database'),
]
