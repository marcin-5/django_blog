from django.contrib import admin

from .models import Tag, Category, Article, Content


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "slug":
            change = request.path.endswith("/change/")
            # show only not published contents when add new article
            kw = {"published": change}
            # do not allow change primary key when edit
            if change:
                kw["slug"] = request.path.split("/")[-3]
                self.readonly_fields = ("slug",)
            kwargs["queryset"] = Content.objects.filter(**kw)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Content)
admin.site.register(Category)
admin.site.register(Tag)
