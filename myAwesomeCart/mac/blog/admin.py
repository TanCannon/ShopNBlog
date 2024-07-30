from django.contrib import admin

# Register your models here
from .models import Blogpost, BlogComment
admin.site.register(Blogpost)
admin.site.register(BlogComment)
