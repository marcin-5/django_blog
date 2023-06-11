from . import views
from django.urls import path


urlpatterns = [
    path("<slug:slug>/<str:thread>/add-post/", views.AddPostView.as_view(), name="api-add-post"),
    path("<slug:slug>/<str:thread>/<int:pk>/", views.PostView.as_view()),
    path("<slug:slug>/add-thread/", views.AddThreadView.as_view(), name="api-add-thread"),
    path("<slug:slug>/<str:thread>/", views.PostListView.as_view()),
    path("<slug:slug>/threads/", views.ThreadListView.as_view()),
]
