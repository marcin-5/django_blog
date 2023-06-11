from django.urls import reverse


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
    client.force_login(user)
    response = client.get(url)
    redirect = client.post(url, data=data)

    assert response.status_code == 200
    assert "<h5>Login Form</h5>" in response.content.decode("UTF-8")

    assert redirect.status_code == 200
    assert redirect.context["user"].is_authenticated is True


def test_register_user(client, db, registration, django_user_model, create_user):
    r = registration()
    url = reverse("users:register-uuid", kwargs={"uuid": r.uuid})
    data = {"email": r.email, "name": "Test User", "password1": "pass1234", "password2": "pass1234"}

    # name too short
    redirect = client.post(url, data={**data, **{"name": "X"}})
    assert redirect.status_code == 200
    assert len(django_user_model.objects.filter(email=data["email"])) == 0
    assert "Name too short." in redirect.content.decode("UTF-8")

    # password missmatch
    redirect = client.post(url, data={**data, **{"password1": "12341234"}})
    assert redirect.status_code == 200
    assert len(django_user_model.objects.filter(email=data["email"])) == 0
    assert "Password missmatch." in redirect.content.decode("UTF-8")

    # password too short
    redirect = client.post(url, data={**data, **{"password1": "1234123", "password2": "1234123"}})
    assert redirect.status_code == 200
    assert len(django_user_model.objects.filter(email=data["email"])) == 0
    assert "Password too short." in redirect.content.decode("UTF-8")

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


def test_send_registration_link(client, create_user):
    user = create_user()
    url = reverse("users:registration")

    response = client.get(url)
    assert response.status_code == 200

    # try to register if user is registered
    response = client.post(url, {"email": user.email, "submit": "Register"})
    assert response.status_code == 302
    response = client.get(response.headers["Location"])
    assert response.status_code == 200

    # try to register new user
    response = client.post(url, {"email": "new@test.xy", "submit": "Register"})
    assert response.status_code == 302
    response = client.get(response.headers["Location"])
    assert response.status_code == 200

    # try to register with wrong email
    response = client.post(url, {"email": "newtest.xy", "submit": "Register"})
    assert response.status_code == 200
    assert "Enter a valid email address." in response.content.decode("UTF-8")


def test_login_and_logout_user(auto_login_user, test_password):
    client, user = auto_login_user()
    url = reverse("users:logout")

    response = client.get(url)
    assert response.status_code == 302
    assert response.headers["Location"] == reverse("home:home")

    url = reverse("users:login")
    response = client.post(url, {"username": user.email, "password": test_password})
    assert response.status_code == 302
    assert response.headers["Location"] == reverse("home:home")
    response = client.get(response.headers["Location"])
    assert response.status_code == 200
    assert response.context["user"].is_authenticated is True
