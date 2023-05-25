import markdown
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView

from home.models import Article, Content


class HomeView(TemplateView):
    template_name = "home/home.html"


class ArticleView(DetailView):
    model = Article
    template_name = "home/article.html"
    content = None

    def get_context_data(self, **kwargs):
        article = super().get_context_data(**kwargs)
        article["content"] = self.content
        return article

    def get_queryset(self):
        self.content = get_object_or_404(Content, slug=self.kwargs["slug"])
        self.content.text = markdown.markdown(self.content.text)
        return Article.objects.filter(slug=self.content, is_active=True)
