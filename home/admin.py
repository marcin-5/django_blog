from django.contrib import admin

from .models import Tag, Category, Article, Content


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "slug":
            kwargs["queryset"] = Content.objects.filter(published=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Content)
admin.site.register(Category)
admin.site.register(Tag)
