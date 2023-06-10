import pytest
from django.core.exceptions import ValidationError

from home.models import Article, Content, Category, Tag


@pytest.mark.django_db
def test_add_content(add_content):
    content = add_content()
    c = Content.objects.filter(slug=content.slug)

    assert len(c) == 1
    assert content.slug == str(c.first())
    with pytest.raises(ValidationError):
        add_content(title="$")


@pytest.mark.django_db
def test_add_category(add_category):
    category = add_category()
    c = Category.objects.filter(name=category.name)

    assert len(c) == 1
    assert category.name == str(c.first())


@pytest.mark.django_db
def test_add_tag(add_tag):
    tag = add_tag()
    t = Tag.objects.filter(name=tag.name)

    assert len(t) == 1
    assert f"#{tag.name}" == str(t.first())


@pytest.mark.django_db
def test_add_article(add_content, add_article):
    content = add_content()
    article = add_article(content=content)

    a = Article.objects.filter(slug=content.slug)
    c = Content.objects.get(slug=article.slug)

    assert len(a) == 1
    assert article.slug_id == str(a.first())
    assert c.published is True
    assert content.slug == str(c)
