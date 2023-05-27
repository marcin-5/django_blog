import markdown
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView

from home.models import Article, Content


class HomeView(TemplateView):
    template_name = "home/home.html"


class ArticleView(DetailView):
    model = Article
    template_name = "home/article.html"
    content = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = self.content
        return context

    def get_queryset(self):
        self.content = get_object_or_404(Content, slug=self.kwargs["slug"])
        self.content.text = markdown.markdown(self.content.text)
        return Article.objects.filter(slug=self.content, is_active=True)


class ArticleListView(ListView):
    model = Article
    template_name = "home/article-list.html"
    ctx = {
        "authors": {},
        "order_fields": {"Date": "published", "Title": "slug__title"},
        # default values for form fields
        "author_id": 0,
        "date_from": "",
        "date_to": "",
        "order_by": "Date",
        "direction": "desc",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.ctx)
        return context

    def get_queryset(self):
        self.ctx.update({key: value for key, value in self.request.POST.items() if key != "csrfmiddlewaretoken"})
        field = self.ctx["order_fields"][self.ctx["order_by"]]
        articles = Article.objects.filter(is_active=True).order_by("-" * (self.ctx["direction"] == "desc") + field)
        self.ctx["authors"] = dict(articles.values_list("author_id", "author__username").distinct())

        if self.ctx["date_from"]:
            articles = articles.filter(published__gte=self.ctx["date_from"])
        if self.ctx["date_to"]:
            articles = articles.filter(published__lte=f'{self.ctx["date_to"]} 23:59')
        if i := int(self.ctx["author_id"] or 0):
            articles = articles.filter(author=i)

        return articles.values_list("slug", "slug__title", "author_id")

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
