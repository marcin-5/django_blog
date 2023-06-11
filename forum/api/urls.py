from . import views
from django.urls import path


urlpatterns = [
    path("<slug:slug>/<str:thread>/", views.PostListView.as_view()),
    path("<slug:slug>/threads/", views.ThreadListView.as_view()),
]
