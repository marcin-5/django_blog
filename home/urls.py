from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("add/", views.ArticleAddView.as_view(), name="article-add"),
    path("list/", views.ArticleListView.as_view(), name="article-list"),
    path("<slug:slug>/", views.ArticleView.as_view()),
]
