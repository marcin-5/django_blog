import re

import markdown
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, FormView

from forum.forms import StartNewThreadForm
from forum.models import Post, Thread
from home.models import Article, Content, Tag, Category
from users.models import CustomUser


class HomeView(TemplateView):
    template_name = "home/home.html"


class ArticleView(DetailView, FormView):
    model = Article
    template_name = "home/article.html"
    form_class = StartNewThreadForm
    content = threads = thread = posts = back = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = self.content
        context["threads"] = self.threads
        context["thread"] = self.thread
        context["posts"] = self.posts
        context["back"] = re.sub(r"^(.*/)[^/]+/", "\\1", self.request.path)
        context["start_new_thread_form"] = StartNewThreadForm()
        return context

    def get_queryset(self):
        self.content = get_object_or_404(Content, slug=self.kwargs["slug"])
        self.content.text = markdown.markdown(self.content.text)
        if thread := self.kwargs.get("thread"):
            self.thread = Thread.objects.filter(id=thread).first()
            self.posts = Post.objects.filter(thread_id=self.thread)
        else:
            self.threads = Thread.objects.filter(slug=self.kwargs["slug"])
        return Article.objects.filter(slug=self.content, is_active=True)

    def form_valid(self, form):
        slug = self.model.objects.filter(slug=self.kwargs["slug"]).first()
        user = CustomUser.objects.filter(name=self.request.user).first()
        thread = form.new_thread_form.save(slug=slug, user=user)
        form.new_post_form.save(thread=thread, user=user)
        return redirect(f"/{slug}/{thread.id}/")


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
        self.ctx["authors"] = dict(articles.values_list("author_id", "author__name").distinct())

        if self.ctx["date_from"]:
            articles = articles.filter(published__gte=self.ctx["date_from"])
        if self.ctx["date_to"]:
            articles = articles.filter(published__lte=f'{self.ctx["date_to"]} 23:59')
        if i := int(self.ctx["author_id"] or 0):
            articles = articles.filter(author=i)

        return articles.values_list("slug", "slug__title", "author_id")

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ArticleAddView(View):
    keys = ("err", "title", "slug", "tags", "selected_categories", "text_file")

    def get(self, request):
        ctx = {key: "" for key in self.keys}
        ctx["categories"] = Category.objects.all()
        return render(request, "home/article-add.html", context=ctx)

    def post(self, request):
        ctx = {key: request.POST.get(key) for key in self.keys[:-2]}
        ctx["selected_categories"] = list(map(int, request.POST.getlist("selected_categories")))
        text = f.read().decode("UTF-8") if (f := request.FILES.get("text_file")) else ""
        ctx["err"] = list()

        if not ctx["title"]:
            ctx["err"].append("Title cannot be empty.")
        if not text:
            ctx["err"].append("Choose a file.")
        if ctx["slug"] and re.search(r"[^a-z-\d]", ctx["slug"]):
            ctx["err"].append("Use only lower case letters, digits and '-' for slug")
        if tags := ctx["tags"].split():
            if wrong_tags := [tag for tag in tags if not re.match(r"#[^\W_]+$", tag)]:
                ctx["err"].append("Wrong tags: " + ", ".join(wrong_tags))
                ctx["err"].append("Tags should start with # and contains alphanumeric chars only")
        if ctx["err"]:
            ctx["categories"] = Category.objects.all()
            return render(request, "home/article-add.html", context=ctx)

        tag_objs = [
            _id if (_id := Tag.objects.filter(name=tag[1:]).first()) else Tag.objects.create(name=tag[1:])
            for tag in tags
        ]
        content = Content.objects.create(slug=ctx["slug"], title=ctx["title"], text=text)
        article = Article.objects.create(slug=content, author=request.user)
        article.tags.set(tag_objs)
        article.categories.set(ctx["selected_categories"])

        return redirect(f"/{article.slug}/")
