import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_api_thread_and_post(api_client, auto_login_user, add_article):
    _, user = auto_login_user()
    api_client.force_login(user=user)
    article = add_article(client=api_client, user=user)
    url = reverse("api-add-thread", kwargs={"slug": article.slug})

    response = api_client.post(url, {"subject": "test api subject"})
    data = response.data
    assert response.status_code == 201
    assert data["started_by"] == user.id

    url = reverse("api-add-post", kwargs={"slug": article.slug, "thread": data["id"]})

    response = api_client.post(url, {"text": "test api comment"})
    assert response.status_code == 201
