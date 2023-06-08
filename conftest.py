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
def user(db, django_db_setup, django_user_model):
    """User instance"""
    return django_user_model.objects.create_user(email="test_user@mail.ru", name="Test User", password="Pass1234")


@pytest.fixture
def registration(db, django_db_setup):
    """User instance"""
    return Registration.objects.create(email="test_user@test.ru")
