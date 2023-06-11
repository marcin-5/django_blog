import pytest

from django.conf import settings
from rest_framework.test import APIClient


from home.models import Article, Content, Category, Tag
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
def api_client():
    client = APIClient()
    return client


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
            kwargs["email"] = "test_user@test.xy"
        if "superuser" in kwargs:
            del kwargs["superuser"]
            return django_user_model.objects.create_superuser(**kwargs)
        else:
            return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def registration(db, django_db_setup):
    """Registration instance"""

    def make_registration(**kwargs):
        if "email" not in kwargs:
            kwargs["email"] = "test_user@test.ru"
        return Registration.objects.create(email=kwargs["email"])

    return make_registration


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.email, password=test_password)
        return client, user

    return make_auto_login


@pytest.fixture
def add_category():
    def make_category(name=None):
        name = name or "This is category"
        category = Category.objects.create(name=name)
        return category

    return make_category


@pytest.fixture
def add_tag():
    def make_tag(name=None):
        name = name or "TestTag"
        tag = Tag.objects.create(name=name)
        return tag

    return make_tag


@pytest.fixture
def add_content():
    def make_content(title=None, text=None):
        title = title or "This is Test Article"
        text = text or "##### Test Article\n---end---"
        content = Content.objects.create(title=title, text=text)
        return content

    return make_content


@pytest.fixture
def add_article(auto_login_user, add_content):
    def make_article(client=None, user=None, content=None):
        if user is None:
            client, user = auto_login_user()
        if content is None:
            content = add_content()

        article = Article.objects.create(author=user, slug=content)
        return article

    return make_article
