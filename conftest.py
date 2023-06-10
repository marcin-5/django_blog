import pytest

from django.conf import settings

from users.models import Registration


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": "localhost",
        "NAME": "external_db",
        "ATOMIC_REQUESTS": True,
    }


@pytest.fixture
def test_password():
    return "test-pass-123"


@pytest.fixture
def create_user(db, django_db_setup, django_user_model, test_password):
    """User instance"""
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "name" not in kwargs:
            kwargs["name"] = "Test User"
        if "email" not in kwargs:
            kwargs["email"] = "test_user@mail.ru"
        if "superuser" in kwargs:
            del kwargs["superuser"]
            return django_user_model.objects.create_superuser(**kwargs)
        else:
            return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def registration(db, django_db_setup):
    """User instance"""
    return Registration.objects.create(email="test_user@test.ru")


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.email, password=test_password)
        return client, user

    return make_auto_login
