from django.contrib import admin
from blog.models import blog_post, post_interactions, Profile

class blog_postadmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'loc_name','subtitle','score', 'author')
admin.site.register(blog_post, blog_postadmin)

class post_interactionsadmin(admin.ModelAdmin):
    list_display = (['interaction_date', 'type','content', 'post_id', 'user_id'])
admin.site.register(post_interactions, post_interactionsadmin)

class Profileadmin(admin.ModelAdmin):
    list_display = (['user'])
admin.site.register(Profile, Profileadmin)

