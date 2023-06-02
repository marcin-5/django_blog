from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("send-registration-link/", views.SendRegistrationLinkView.as_view()),
    path("send-registration-link/done/", views.SendRegistrationLinkView.as_view(), name="link-sent"),
    path("register/<uuid>/", views.RegisterUserView.as_view()),
]
