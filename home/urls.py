from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("add/", views.ArticleAddView.as_view(), name="article-add"),
    path("list/", views.ArticleListView.as_view(), name="article-list"),
    path("<slug:slug>/", views.ArticleView.as_view()),
    path("<slug:slug>/new-thread/", views.ArticleView.as_view()),
    path("<slug:slug>/<str:thread>/", views.ArticleThreadView.as_view()),
    path("<slug:slug>/<str:thread>/<int:pid>/", views.ArticleThreadView.as_view()),
]
