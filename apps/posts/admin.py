from django.contrib import admin

from apps.posts.models import Tag, Post, Comment


admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
