from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("list/", views.ArticleListView.as_view()),
    path("<slug:slug>/", views.ArticleView.as_view()),
]