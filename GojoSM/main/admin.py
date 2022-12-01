from django.contrib import admin
from .models import UserProfile, Following, Post
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Following)
admin.site.register(Post)