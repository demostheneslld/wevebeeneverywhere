"""
Definition of views.
"""

import uuid
from datetime import datetime

from azure.storage.blob import BlobServiceClient, __version__
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import (BlogPostFilterForm, BlogPostForm, ProfileForm,
                        RegisterForm, SubscribeForm, UnsubscribeForm, UserForm)
from blog.models import BlogPost, MediaItem, PostInteraction

import environment

# CONSTANTS
UPPER_BLOG_POST_FORM_FIELDS = [
    'title',
    'subtitle',
    'participants',
    'loc_name',
    'lat',
    'lng',
    'score',
    'event_date',
    'publish_date',
]

LOWER_BLOG_POST_FORM_FIELDS = [
    'content',
]

# HELPER FUNCTIONS


def getposts(request, topx=None, sort='-publish_date', post_id='all', author='all', published_only=True):
  posts = BlogPost.objects.all().order_by(sort).defer('content')

  if str(post_id) != 'all':
    posts = posts.filter(id=post_id)

  if str(author) != 'all':
    posts = posts.filter(author=author)

  if published_only:
    posts = posts.filter(publish_date__lte=datetime.now())

  if isinstance(topx, int):
    posts = posts[:topx]
  return posts


def action(request):
  request_type = request.GET.get('type', '')
  target = request.GET.get('target', '')
  details = request.GET.get('details', '')
  current_user = None
  if request.user.is_authenticated:
    current_user = request.user
  if request_type == "like":
    newlike = PostInteraction(
        user_id=current_user,
        post_id=getposts(request, post_id=target)[0],
        type=request_type)
    newlike.save()
    return redirect('/stories?id=' + target)
  elif request_type == "comment":
    comment = PostInteraction(
        user_id=request.user,
        post_id=getposts(request, post_id=target)[0],
        content=details,
        type=request_type)
    comment.save()
    return redirect('/stories?id=' + target)
  elif request_type == "deletecomment":
    comment = PostInteraction(
        id=target,
        content=details,
        type='comment')
    comment.delete()
    return redirect('/stories?id=' + details)
  else:
    raise Exception('Unknown Request Type')

# PUBLIC PAGES


def home(request):
  assert isinstance(request, HttpRequest)
  story_count = getposts(request).count()
  return render(
      request,
      'app/views/index.html',
      {
          'title': 'Home',
          'description': 'Explore everywhere with us!',
          'og_type': 'website',
          'og_image': 'http://i.imgur.com/wISv7LI.png',
          'story_count': story_count,
      }
  )


def travel_map(request):
  assert isinstance(request, HttpRequest)
  posts = getposts(request, sort='publish_date')
  # Only take posts with lat/lng to not break map
  posts = posts.filter(lat__isnull=False)
  posts = posts.filter(lng__isnull=False)
  return render(
      request,
      'app/views/map.html',
      {
          'title': 'Map',
          'description': 'Map of our adventures!',
          'og_type': 'website',
          'og_image': 'http://i.imgur.com/wISv7LI.png',
          'posts': posts,
          'google_maps_api_key': environment.GOOGLE_MAPS_API_KEY,
      }
  )


def stories(request):
  assert isinstance(request, HttpRequest)
  # page basics
  post_id = request.GET.get('id', 'all')
  topx = request.GET.get('topx', 15)
  title = 'Stories'
  description = 'Chronicling the adventures of Molly and Nathan as we venture across the world.'
  og_type = 'website'
  post_list = getposts(request, topx=topx)
  og_image = 'http://i.imgur.com/wISv7LI.png'

  # get main post
  if post_id == 'all':
    posts = getposts(request)[0:5]
  else:
    posts = getposts(request, post_id=post_id)

  # if only one post meets criteria, optimize seo
  if posts.count() == 1:
    title = posts[0].title
    description = posts[0].subtitle
    og_type = 'article'
    try:
      og_image = posts[0].content.split('<img')[1].split('src="')[
          1].split('"')[0]
    # pylint: disable=broad-except
    except Exception:
      pass

  posts_with_liked = []

  for post in posts:
    if request.user.is_authenticated:
      posts_with_liked.append((
          post,
          PostInteraction.objects.all().filter(
              type='like', user_id=request.user, post_id=post.id)
      ))
    else:
      posts_with_liked.append((post, False))

  return render(
      request,
      'app/views/stories.html',
      {
          'title': title,
          'description': description,
          'og_type': og_type,
          'og_image': og_image,
          'post_list': post_list,
          'posts': posts_with_liked,
          'current_user': request.user,
      }
  )


def storyfinder(request):
  assert isinstance(request, HttpRequest)

  title = 'Story Finder'
  description = 'Chronicling the adventures of Molly and Nathan as we venture across the world.'
  og_type = 'website'
  og_image = 'http://i.imgur.com/wISv7LI.png'

  post_list = getposts(request)
  form = BlogPostFilterForm(request.GET)
  return render(
      request,
      'app/views/storyfinder.html',
      {
          'title': title,
          'description': description,
          'og_type': og_type,
          'og_image': og_image,
          'post_list': post_list,
          'form': form
      }
  )


def sitemap(request):
  assert isinstance(request, HttpRequest)
  post_list = getposts(request)
  return render(
      request,
      'app/views/sitemap.html',
      {
          'post_list': post_list,
      }
  )

# POST MANAGEMENT
# Manage Post List


@permission_required('blog_post.add_blog_post')
def manage_blog_post_list(request):
  assert isinstance(request, HttpRequest)
  post_list = getposts(request, author=request.user, published_only=False)

  return render(
      request,
      'app/views/manage_blog_post_list.html',
      {
          'post_list': post_list,
          'post_count': len(post_list),
      }
  )

# Add Post


@permission_required('blog_post.add_blog_post')
def manage_blog_post_add(request):
  assert isinstance(request, HttpRequest)
  post = BlogPost(
      author=request.user
  )
  post.save()
  return redirect('manage_blog_post_change', pk=post.pk)

# Change Post


@permission_required('blog_post.change_blog_post')
def manage_blog_post_change(request, pk):
  assert isinstance(request, HttpRequest)
  post = get_object_or_404(BlogPost, pk=pk)
  if request.user == post.author:
    if request.method == "POST":
      form = BlogPostForm(request.POST, instance=post)
      if form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect(manage_blog_post_list)
    else:
      form = BlogPostForm(instance=post)
    return render(
        request,
        'app/views/manage_blog_post.html',
        {
            'blog_post_form': form,
            'upper_fields': UPPER_BLOG_POST_FORM_FIELDS,
            'lower_fields': LOWER_BLOG_POST_FORM_FIELDS,
            'post': post,
            'title': 'Edit Post: ' + (post.title or 'Untitled')
        }
    )
  else:
    return redirect('manage_blog_post_list')

# Upload Image to Post


@permission_required('blog_post.change_blog_post')
def manage_blog_post_upload_image(request, pk):
  assert isinstance(request, HttpRequest)
  if not request.method == 'POST':
    raise Exception('Invalid HTTP Method. POST is Required')
  post = get_object_or_404(BlogPost, pk=pk)
  file = request.FILES['upload']
  file_ext = file.name.split('.')[-1]
  file_name = f'''{uuid.uuid4()}.{file_ext}'''
  source_url = f'''https://wevebeeneverywhere.blob.core.windows.net/media/{ file_name }'''
  # Create a blob client using the local file name as the name for the blob
  connect_str = environment.AZURE_STORAGE_CONNECTION_STRING
  blob_service_client = BlobServiceClient.from_connection_string(connect_str)
  blob_client = blob_service_client.get_blob_client(
      container='media', blob=file_name)

  print("\nUploading to Azure Storage as blob:\n\t" + file_name)

  # Upload the created file
  with file.open() as data:
    blob_client.upload_blob(data)
  data = {
      'url': source_url
  }
  # Save Media Item to Database
  media_item = MediaItem()
  media_item.post_id = post
  media_item.media_type = 'picture'
  media_item.caption = ''
  media_item.file_name = file_name.replace('.' + file_ext, '')
  media_item.file_extension = file_ext.lower()
  media_item.source_url = source_url
  media_item.save()
  return JsonResponse(data)

# Delete Post


@permission_required('blog_post.change_blog_post')
def manage_blog_post_delete(request, pk):
  assert isinstance(request, HttpRequest)
  post = get_object_or_404(BlogPost, pk=pk)
  if request.user == post.author:
    post.delete()
  return redirect('manage_blog_post_list')

# Email Subscribers


@permission_required('blog_post.change_blog_post')
def manage_blog_post_email_subscribers(request, pk):
  assert isinstance(request, HttpRequest)
  post = get_object_or_404(BlogPost, pk=pk)
  if request.user == post.author:
    emails_sent = post.send_email()
    messages.success(request, "Emailed " +
                     str(emails_sent) + " subscriber(s)")
  return redirect('manage_blog_post_list')

# Publish Post


@permission_required('blog_post.change_blog_post')
def manage_blog_post_publish(request, pk):
  assert isinstance(request, HttpRequest)
  post = get_object_or_404(BlogPost, pk=pk)
  if request.user == post.author:
    errors = post.strict_validate()
    if len(errors) > 0:
      messages.error(
          request, "Unable to publish. Please correct these errors: " + ', '.join(errors))
    else:
      post.publish()
      messages.success(request, "Post has been published!")
  return redirect('manage_blog_post_list')

# Download Database


@user_passes_test(lambda u: u.is_superuser)
def download_database(request):
  db_path = settings.DATABASES['default']['NAME']
  dbfile = File(open(db_path, "rb"))
  response = HttpResponse(dbfile, content_type='application/x-sqlite3')
  response['Content-Disposition'] = 'attachment; filename=wbe_db.sqlite3'
  response['Content-Length'] = dbfile.size
  return response

# STATIC VIEWS


def contact(request):
  assert isinstance(request, HttpRequest)
  return render(
      request,
      'app/views/contact.html',
      {
          'title': 'Contact',
          'message': 'Get in touch!',
          'description': 'Get in touch!',
          'og_type': 'website',
          'og_image': 'http://i.imgur.com/wISv7LI.png',
      }
  )


def privacy(request):
  assert isinstance(request, HttpRequest)
  return render(
      request,
      'app/views/_privacy.html',
      {
          'title': 'Privacy',
          'og_type': 'website',
          'og_image': 'http://i.imgur.com/wISv7LI.png',
      }
  )


def terms(request):
  assert isinstance(request, HttpRequest)
  return render(
      request,
      'app/views/_terms.html',
      {
          'title': 'Terms of Service',
          'og_type': 'website',
          'og_image': 'http://i.imgur.com/wISv7LI.png',
      }
  )


# Authentication

def register(request):
  form = RegisterForm()
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, "Registration successful")
      return redirect("profile")
    messages.error(
        request, "Unsuccessful registration: Invalid information")
  return render(request=request, template_name="registration/register.html", context={"register_form": form})


def subscribe(request):
  form = SubscribeForm()
  if request.method == "POST":
    form = SubscribeForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Subscription successful")
      return redirect("home")
    messages.error(
        request, "Unsuccessful subscription: Invalid information")
  return render(request=request, template_name="registration/subscribe.html", context={"subscribe_form": form})


def unsubscribe(request):
  form = UnsubscribeForm()
  if request.method == "POST":
    email = request.POST.get('email')
    user = get_object_or_404(User, email=email)
    if user:
      form = UnsubscribeForm(request.POST, instance=user)
      if form.is_valid():
        user.profile.is_subscribed_to_emails = False
        user.save()
        messages.success(request, "Unsubscribe successful")
        return redirect("home")
      messages.error(
          request, "Unsuccessful unsubscribe: Invalid information")
    else:
      messages.error(
          request, 'Unsuccessful unsubscribe: No user exists with that email')
  return render(request=request, template_name="registration/unsubscribe.html", context={"unsubscribe_form": form})


@login_required()
def profile(request):
  user = request.user
  user_form = UserForm(instance=user)
  profile_form = ProfileForm(instance=user.profile)
  if request.method == "POST":
    user_form = UserForm(request.POST, instance=user)
    profile_form = ProfileForm(request.POST, instance=user.profile)
    if all((user_form.is_valid(), profile_form.is_valid())):
      saved_profile = profile_form.save()
      user = user_form.save(commit=False)
      user.profile = saved_profile
      user.save()
      messages.success(request, "Profile update successful")
      return redirect("home")
    messages.error(
        request, "Unsuccessful Profile Update: Invalid information")
  return render(request=request, template_name="registration/profile.html", context={
      "user_form": user_form,
      "profile_form": profile_form
  })
