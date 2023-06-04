from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("register/", views.SendRegistrationLinkView.as_view(), name="registration"),
    path("link-sent/", views.SendRegistrationLinkView.as_view(), name="link-sent"),
    path("register/<uuid>/", views.RegisterUserView.as_view()),
]
