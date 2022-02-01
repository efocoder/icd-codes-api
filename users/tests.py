import pytest
from django.db.models import QuerySet
from rest_framework import status

from users.models import User, Category


@pytest.mark.django_db()
def test_create_user(create_user_fixture):
    user = User.objects.filter(status="ACTIVE")
    assert isinstance(user, QuerySet)
    assert len(user) == 1
    assert isinstance(user[0], User)


@pytest.mark.django_db(transaction=True)
def test_create_category(create_category_fixture, create_user_fixture):
    cat = Category.objects.filter(status='ACTIVE')
    assert isinstance(cat, QuerySet)
    assert isinstance(cat[0], Category)
    assert cat[0].created_by == create_user_fixture


@pytest.mark.django_db()
def test_list_categories(create_category_fixture):
    cats = Category.objects.filter(status="ACTIVE")
    assert isinstance(cats, QuerySet)
    assert len(cats) == 1
    assert isinstance(cats[0], Category)


@pytest.mark.django_db()
def test_login(login_user):
    assert login_user['status'] == status.HTTP_200_OK
    assert isinstance(login_user['message'], str)
    assert login_user['message'] == "Login Successful"
    assert isinstance(login_user['output'], dict)
    assert 'access_token' in login_user['output']
