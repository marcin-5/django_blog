from django.contrib import admin

from .models import Tag, Category, Article, Content


admin.site.register(Article)
admin.site.register(Content)
admin.site.register(Category)
admin.site.register(Tag)
