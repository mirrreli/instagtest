from django.contrib import admin
from post.models import Post, Follow, Stream

admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)