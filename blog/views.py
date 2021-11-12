"""
Definition of views.
"""

from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.http import HttpRequest
from blog.models import BlogPost, PostInteraction
from blog.forms import BlogPostForm, BlogPostFilterForm, MediaItemForm
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

# PAGE VIEWS
def home(request):
    assert isinstance(request, HttpRequest)
    story_count = getposts(request).count()
    return render(
        request,
        'app/views/index.html',
        {
            'title':'Home',
            'description': 'Explore everywhere with us!',
            'og_type': 'website',
            'og_image': 'http://i.imgur.com/wISv7LI.png',
            'story_count': story_count,
            'year':datetime.now().year,
        }
    )

def travel_map(request):
    assert isinstance(request, HttpRequest)
    posts = getposts(request, sort='publish_date')
    return render(
        request,
        'app/views/map.html',
        {
            'title':'Map',
            'description' : 'Map of our adventures!',
            'og_type': 'website',
            'og_image': 'http://i.imgur.com/wISv7LI.png',
            'year':datetime.now().year,
            'posts':posts,
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
            og_image = posts[0].content.split('<img')[1].split('src="')[1].split('"')[0]
        # pylint: disable=broad-except
        except Exception:
            pass

    posts_with_liked = []

    for post in posts:
        if request.user.is_authenticated:
            posts_with_liked.append((
                post,
                PostInteraction.objects.all().filter(type='like', user_id=request.user, post_id=post.id)
            ))
        else:
            posts_with_liked.append((post, False))

    return render(
        request,
        'app/views/stories.html',
        {
            'title' : title,
            'description' : description,
            'og_type': og_type,
            'og_image': og_image,
            'year' : datetime.now().year,
            'post_list' : post_list,
            'posts' : posts_with_liked,
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
            'title' : title,
            'description' : description,
            'og_type': og_type,
            'og_image': og_image,
            'year' : datetime.now().year,
            'post_list' : post_list,
            'form' : form
        }
    )

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/views/contact.html',
        {
            'title':'Contact',
            'message':'Get in touch!',
            'description': 'Get in touch!',
            'og_type': 'website',
            'og_image': 'http://i.imgur.com/wISv7LI.png',
            'year':datetime.now().year,
        }
    )

def sitemap(request):
    assert isinstance(request, HttpRequest)
    post_list = getposts(request)
    return render(
        request,
        'app/views/sitemap.html',
        {
            'post_list' : post_list,
            'year':datetime.now().year,
        }
    )

# SITE MANAGEMENT
@permission_required('blog_post.add_blog_post')
def manage_blog_post_list(request):
    assert isinstance(request, HttpRequest)
    post_list = getposts(request, author=request.user, published_only=False)

    return render(
        request,
        'app/views/manage_blog_post_list.html',
        {
            'post_list' : post_list,
        }
    )

@permission_required('blog_post.add_blog_post')
def manage_blog_post_add(request):
    assert isinstance(request, HttpRequest)
    post = None
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('manage_blog_post_change', pk=post.pk)
    else:
        form = BlogPostForm()
        post = form.save(commit = False)
    return render(
        request,
        'app/views/manage_blog_post.html',
        {
            'blog_post_form': form,
            'media_item_form': MediaItemForm(),
            'upper_fields': UPPER_BLOG_POST_FORM_FIELDS,
            'lower_fields': LOWER_BLOG_POST_FORM_FIELDS,
            'post': post,
            'title': 'Add Post'
        }
    )

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
                'media_item_form': MediaItemForm(),
                'upper_fields': UPPER_BLOG_POST_FORM_FIELDS,
                'lower_fields': LOWER_BLOG_POST_FORM_FIELDS,
                'post': post,
                'title': 'Edit Post: ' + post.title
            }
        )
    else:
        return redirect('manage_blog_post_list')

@permission_required('blog_post.delete_blog_post')
def manage_blog_post_delete(request, pk):
    assert isinstance(request, HttpRequest)
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('manage_blog_post_list')

# STATIC VIEWS
def privacy(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/views/_privacy.html',
        {
            'title':'Privacy',
            'og_type': 'website',
            'og_image': 'http://i.imgur.com/wISv7LI.png',
            'year':datetime.now().year,
        }
    )

def terms(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/views/_terms.html',
        {
            'title':'Terms of Service',
            'og_type': 'website',
            'og_image': 'http://i.imgur.com/wISv7LI.png',
            'year':datetime.now().year,
        }
    )
