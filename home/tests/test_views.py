import os

import pytest
from django.urls import reverse


def test_view_home(client, db):
    url = reverse("home:home")
    response = client.get(url)

    assert response.status_code == 200
    assert "<h1>Home</h1>" in response.content.decode("UTF-8")


@pytest.mark.django_db
def test_article_add(auto_login_user):
    client, user = auto_login_user()
    user.can_publish = True
    user.save()
    txt_file = os.path.join(os.path.dirname(__file__), "test_article.txt")
    url = reverse("home:article-add")

    response = client.get(url)
    assert response.status_code == 200
    assert "<title>Add new article" in response.content.decode("UTF-8")

    # no file selected
    response = client.post(url, {"title": "Test Title"})
    assert response.status_code == 200
    assert "Choose a file." in response.content.decode("UTF-8")

    # wrong slug
    with open(txt_file) as tf:
        response = client.post(url, {"title": "Test Title", "text_file": tf, "slug": "$$$"})
    assert response.status_code == 200
    assert "Use only lower case letters, " in response.content.decode("UTF-8")

    # no title
    with open(txt_file) as tf:
        response = client.post(url, {"title": "", "text_file": tf, "slug": "test"})
    assert response.status_code == 200
    assert "Title cannot be empty." in response.content.decode("UTF-8")

    # wrong tag
    with open(txt_file) as tf:
        response = client.post(url, {"title": "Test Title", "text_file": tf, "tags": "@2 /test"})
    assert response.status_code == 200
    assert "Tags should start with #" in response.content.decode("UTF-8")
    assert "Wrong tags: @2, /test<br>" in response.content.decode("UTF-8")

    # correct data
    with open(txt_file) as tf:
        response = client.post(url, {"title": "Test Title", "text_file": tf, "tags": "#one #two"})
    assert response.status_code == 302
    response = client.get(response.headers["Location"])
    assert response.status_code == 200
    assert "<h5>test article</h5>" in response.content.decode("UTF-8")


@pytest.mark.django_db
def test_article_list(auto_login_user, add_article):
    client, user = auto_login_user()
    article = add_article(client=client, user=user)
    url = reverse("home:article-list")
    response = client.get(url)
    assert response.status_code == 200
    assert f'href="/{article.slug}/"' in response.content.decode("UTF-8")
    assert f'value="{user.id}">{user.name}<' in response.content.decode("UTF-8")


@pytest.mark.django_db
def test_article_thread(auto_login_user, add_article):
    client, user = auto_login_user()
    article = add_article(client=client, user=user)
    url = f"/{article.slug}/"

    response = client.get(url)
    assert response.status_code == 200
    assert "Add thread" in response.content.decode("UTF-8")

    response = client.post(url, {"subject": "101", "text": "comment"})
    assert response.status_code == 302
    response = client.get(response.headers["Location"])
    assert response.status_code == 200
