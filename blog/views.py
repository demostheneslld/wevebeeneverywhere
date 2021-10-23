"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.http import HttpRequest
from blog.models import blog_post
from blog.models import post_interactions
from blog.forms import BlogPostForm
from blog.forms import BlogPostFilterForm

# HELPER FUNCTIONS
def getposts(request, topx=None, sort='-publish_date', id='all', author='all', PublishedOnly=True):
    posts = blog_post.objects.all().order_by(sort).defer('content')

    if str(id) != 'all':
        posts = posts.filter(id=id)

    if str(author) != 'all':
        posts = posts.filter(author=author)

    if (PublishedOnly):
        posts = posts.filter(publish_date__lte=datetime.now())
    
    if isinstance(topx, int):
        posts = posts[:topx]
    return posts

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def action(request):
    request_type = request.GET.get('type', '')
    target = request.GET.get('target', '')
    details = request.GET.get('details', '')
    current_user = None
    if request.user.is_authenticated:
        current_user = request.user
    if request_type == "like":
        newlike = post_interactions( 
            user_id=current_user,
            post_id=getposts(request, id=target)[0],
            request_type=request_type)
        newlike.save()
        return redirect('/stories?id=' + target)
    if type == "comment":
        comment = post_interactions(
            user_id=request.user,
            post_id=getposts(request, id=target)[0],
            content=details,
            request_type=request_type)
        comment.save()
        return redirect('/stories?id=' + target)
    else:
        pass

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

def map(request):
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
        }
    )

def stories(request):
    assert isinstance(request, HttpRequest)
    # page basics
    id = request.GET.get('id','all')
    topx = request.GET.get('topx', 15)
    title = 'Stories'
    description = 'Chronicling the adventures of Molly and Nathan as we venture across the world.' 
    og_type = 'website'
    post_list = getposts(request, topx = topx)
    og_image = 'http://i.imgur.com/wISv7LI.png'

    # get main post
    if (id == 'all'):
        posts = getposts(request)[0:5]
    else:
        posts = getposts(request, id=id)

    # if only one post meets criteria, optimize seo
    if (posts.count() == 1):
        title = posts[0].title 
        description = posts[0].subtitle
        og_type = 'article'
        try:
            og_image = posts[0].content.split('<img')[1].split('src="')[1].split('"')[0]
        except:
            pass

    posts_with_liked = []

    for post in posts:
        if request.user.is_authenticated:
            posts_with_liked.append((post,
            post_interactions.objects.all().filter(type='like', user_id = request.user, post_id = post.id)))
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
    post_list = getposts(request, author=request.user, PublishedOnly=False)

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
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('manage_blog_post_change', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'app/views/manage_blog_post.html', 
                    {
                    'BlogPostForm': form
                    , 'title': 'Add Post'
                    }
                  )

@permission_required('blog_post.change_blog_post')
def manage_blog_post_change(request, pk):
    assert isinstance(request, HttpRequest)
    post = get_object_or_404(blog_post, pk=pk)
    if (request.user == post.author):
        if request.method == "POST":
            form = BlogPostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect(manage_blog_post_list)
        else:
            form = BlogPostForm(instance = post)
            return render(request
                          , 'app/views/manage_blog_post.html', 
                            {
                            'BlogPostForm': form
                            , 'title': 'Edit Post: ' + post.title
                            }
                          )
    else:
        return redirect('manage_blog_post_list')    

@permission_required('blog_post.delete_blog_post')
def manage_blog_post_delete(request, pk):
    assert isinstance(request, HttpRequest)
    post = get_object_or_404(blog_post, pk=pk)
    if (request.user == post.author):
        post.delete()
    return redirect('manage_blog_post_list') 

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
