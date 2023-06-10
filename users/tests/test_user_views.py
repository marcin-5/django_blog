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
    url = reverse("users:register-uuid", kwargs={"uuid": registration.uuid})
    data = {"email": registration.email, "name": "Test User", "password1": "pass1234", "password2": "pass1234"}

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

    # email already registered #FIXME
    test_user = create_user()
    redirect = client.post(url, data={**data, **{"email": test_user.email}})
    assert redirect.status_code == 200
    test_user.delete()

    redirect = client.post(url, data=data)
    user = django_user_model.objects.get(email=data["email"])

    assert redirect.status_code == 302
    assert user.name == data["name"]

    response = client.get(redirect.url)
    assert response.status_code == 200
    assert "<h5>Login Form</h5>" in response.content.decode("UTF-8")

    assert str(registration) == f"{registration.uuid} - {registration.email}"


# @pytest.mark.django_db
# def test_form_valid_registration(create_user):
#     user = create_user()
#     request = factory.post(reverse("users:registration"), data={"email": user.email})
#     request = factory.post(reverse("users:registration"), data={"email": "a@a.pl"})


# @pytest.mark.django_db
# def test_form_valid_login(create_user):
#     user = create_user()
#     request = factory.post(reverse("users:login"), data={"username": user.email, "password": user.password})
#     request.user = user
#     response = login_view(request)
#
#     assert response.status_code == 200
