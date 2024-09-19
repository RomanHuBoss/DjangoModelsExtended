from django.contrib import admin
from .models import Author, Category, Post, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
