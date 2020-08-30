from django.contrib import admin

from blog.models import BlogPost, Like

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Like)