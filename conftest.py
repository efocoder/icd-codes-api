import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate

from codes.views import CodesView
from users.models import User, Category
from users.views import LoginView
from utility.response_renderer_test import render_response_and_send_content

factory = APIRequestFactory()
client = APIClient()


@pytest.fixture
def create_user_fixture(db):
    user = User.objects.create(email='clem.clem@gmail.com', password='password', username="test",
                               first_name="Hello",
                               last_name="world", status="ACTIVE")
    user.save()

    return user


@pytest.fixture
def create_category_fixture(db, create_user_fixture):
    cat = Category.objects.create(category_code="AAA", description="Test Description", created_by=create_user_fixture)
    cat.save()

    return cat


@pytest.fixture
def login_user(db, create_user_fixture):
    data = {
        "email": create_user_fixture.email,
        "password": "password"
    }
    request = factory.post(reverse('login'), data=data)
    res = LoginView.as_view()(request)
    content = render_response_and_send_content(res)

    return content


@pytest.fixture
def create_icd_code_fixture(create_user_fixture, create_category_fixture, login_user):
    data = {
        "icd_code": "A024",
        "description": "Test",
        "icd_code_prefix": "0",
        "category": create_category_fixture.pk
    }

    request = factory.post(reverse('codes'), data=data, format='json')
    force_authenticate(request, user=create_user_fixture, token=login_user['output']['access_token'])

    res = CodesView.as_view()(request)
    content = render_response_and_send_content(res)

    return content
