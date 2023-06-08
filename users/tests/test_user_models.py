import pytest


@pytest.mark.slow
def test_create_user(user, django_user_model):

    users = django_user_model.objects.filter(email='test_user@mail.ru')

    assert len(users) == 1
    assert users.first().name == 'Test User'


@pytest.mark.smoke
@pytest.mark.slow
def test_change_password(user):

    password = '5678Pass'
    user.set_password(password)

    assert user.check_password(password) is True
