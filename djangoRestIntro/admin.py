from django.contrib import admin
from .models import User, Post

# REGISTERING MODELS to the admin panel
# WAY 1: register the model as is
admin.site.register(User)


# WAY 2: make a custom ModelAdmin
@admin.register(Post)  # Method 1: register ModelAdmin through annotation
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'date_posted', 'author')
    list_filter = ('date_posted', 'author')
    search_fields = ('title', 'content')

# Method 2: register ModelAdmin
# admin.site.register(Post, PostAdmin)
