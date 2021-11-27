from django.contrib import admin
from blog.models import BlogPost, MediaItem, PostInteraction, Profile

class blog_postadmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'loc_name','subtitle','score', 'author')
admin.site.register(BlogPost, blog_postadmin)

class media_item_admin(admin.ModelAdmin):
    list_display = ('post_id', 'media_type', 'caption','file_name','file_extension', 'source_url')
admin.site.register(MediaItem, media_item_admin)

class post_interactionsadmin(admin.ModelAdmin):
    list_display = (['interaction_date', 'type','content', 'post_id', 'user_id'])
admin.site.register(PostInteraction, post_interactionsadmin)

class Profileadmin(admin.ModelAdmin):
    list_display = (['user'])
admin.site.register(Profile, Profileadmin)

