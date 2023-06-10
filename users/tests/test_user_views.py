import pytest

from django.test import RequestFactory
from django.urls import reverse

from users.models import CustomUser
from users.views import SendRegistrationLinkView, login_view

factory = RequestFactory()


def test_registration_page(client, db):
    url = reverse("users:registration")

    response = client.get(url)

    assert response.status_code == 200
    assert '<input class="my-2 form-control-sm" type="submit" value="Register">' in response.content.decode("UTF-8")


def test_login_page(client, create_user, db, django_user_model):
    user = create_user()
    url = reverse("users:login")
    data = {"username": user.email,
            "password": user.password,
            "name": user.name}
    response = client.get(url)
    redirect = client.post(url, data=data)
    user = django_user_model.objects.get(email=data["username"])

    assert response.status_code == 200
    assert "<h5>Login Form</h5>" in response.content.decode("UTF-8")

    assert redirect.status_code == 200
    assert user.name == data["name"]


def test_register_user(client, db, registration, django_user_model, create_user):
    r = registration()
    url = reverse("users:register-uuid", kwargs={"uuid": r.uuid})
    data = {"email": r.email, "name": "Test User", "password1": "pass1234", "password2": "pass1234"}

    # name too short
    redirect = client.post(url, data={**data, **{"name": "X"}})
    assert redirect.status_code == 200
    assert len(django_user_model.objects.filter(email=data["email"])) == 0

    # password missmatch
    redirect = client.post(url, data={**data, **{"password1": "12341234"}})
    assert redirect.status_code == 200
    assert len(django_user_model.objects.filter(email=data["email"])) == 0

    # password too short
    redirect = client.post(url, data={**data, **{"password1": "1234123", "password2": "1234123"}})
    assert redirect.status_code == 200
    assert len(django_user_model.objects.filter(email=data["email"])) == 0

    redirect = client.post(url, data=data)
    user = django_user_model.objects.get(email=data["email"])

    assert redirect.status_code == 302
    assert user.name == data["name"]

    response = client.get(redirect.url)
    assert response.status_code == 200
    assert "<h5>Login Form</h5>" in response.content.decode("UTF-8")

    assert str(r) == f"{r.uuid} - {r.email}"

    # email already registered
    r = registration()
    url = reverse("users:register-uuid", kwargs={"uuid": r.uuid})
    redirect = client.post(url, data={**data, **{"email": r.email, "name": "abc def"}})
    assert redirect.status_code == 200
    assert "This email is registered already." in redirect.content.decode("UTF-8")
