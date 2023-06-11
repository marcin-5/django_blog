import pytest

from django.urls import reverse


@pytest.mark.slow
def test_create_user(create_user, django_user_model):
    with pytest.raises(ValueError):
        create_user(email="")

    with pytest.raises(ValueError):
        create_user(name="")

    user = create_user()
    users = django_user_model.objects.filter(email="test_user@test.xy")

    assert len(users) == 1
    assert users.first().name == user.name
    user.delete()

    user = create_user(superuser=True)
    users = django_user_model.objects.filter(email="test_user@test.xy")

    assert len(users) == 1
    assert str(users.first()) == user.name


@pytest.mark.smoke
@pytest.mark.slow
def test_change_password(create_user):
    user = create_user()
    password = "5678Pass"
    user.set_password(password)

    assert user.check_password(password) is True


@pytest.mark.django_db
def test_auth_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse("users:login")
    response = client.get(url)
    assert response.status_code == 200
    assert f'<a class="nav-link" href="">{user.name}</a>' in response.content.decode("UTF-8")
