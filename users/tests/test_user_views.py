from django.urls import reverse


def test_registration_page(client, db):
    url = reverse("users:registration")

    response = client.get(url)

    assert response.status_code == 200
    assert '<input class="my-2 form-control-sm" type="submit" value="Register">' in response.content.decode("UTF-8")


def test_login_page(client, create_user, db, django_user_model):
    url = reverse("users:login")
    data = {"username": create_user.email,
            "password": create_user.password,
            "name": create_user.name}
    response = client.get(url)
    redirect = client.post(url, data=data)
    user = django_user_model.objects.get(email=data["username"])

    assert response.status_code == 200
    assert "<h5>Login Form</h5>" in response.content.decode("UTF-8")

    assert redirect.status_code == 200
    assert user.name == data["name"]


def test_register_user(client, db, registration, django_user_model):
    url = reverse("users:register-uuid", kwargs={"uuid": registration.uuid})
    data = {"email": registration.email, "name": "Test User", "password1": "pass1234", "password2": "pass1234"}

    redirect = client.post(url, data=data)
    user = django_user_model.objects.get(email=data["email"])

    assert redirect.status_code == 302
    assert user.name == data["name"]

    response = client.get(redirect.url)
    assert response.status_code == 200
    assert "<h5>Login Form</h5>" in response.content.decode("UTF-8")

