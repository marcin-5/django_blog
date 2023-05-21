from . import views
from django.urls import path


urlpatterns = [path("hello/", views.hello_world, name="hello_world")]
