from . import views
from django.urls import path


urlpatterns = [
    path("hello/", views.hello_world, name="hello_world"),
    path("list/", views.ArticleListView.as_view()),
    path("<slug:slug>/", views.ArticleView.as_view()),
]
