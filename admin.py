from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    #display of posts for admin users to moderate posts
    list_display = ['title', 'topic','content','created_by']
    list_filter = ("topic",)
    search_fields = ['title', 'content'] 

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    #display of comments for admin users to moderate posts
    list_display = ['post', 'message', 'created_by']
    list_filter = ("created_at",)
    search_fields = ['post','message']
admin.site.register(Comment, CommentAdmin)