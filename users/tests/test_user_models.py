import pytest


@pytest.mark.slow
def test_create_user(create_user, django_user_model):

    users = django_user_model.objects.filter(email='test_user@mail.ru')

    assert len(users) == 1
    assert users.first().name == 'Test User'


@pytest.mark.smoke
@pytest.mark.slow
def test_change_password(create_user):

    password = '5678Pass'
    create_user.set_password(password)

    assert create_user.check_password(password) is True
