import pytest
from django.urls import reverse
from rest_framework.test import force_authenticate

from codes.views import CodesView
from conftest import factory
from utility.response_renderer_test import render_response_and_send_content


@pytest.mark.django_db()
class TestCode:
    def test_list_codes_without_credentials(self):
        request = factory.get(reverse("codes"))
        res = CodesView.as_view()(request)
        content = render_response_and_send_content(res)
        assert isinstance(content, dict)
        assert 'detail' in content
        assert content['detail'] == 'Authentication credentials were not provided.'

    def test_list_codes_with_credentials_and_with_no_data(self, create_user_fixture, login_user):
        request = factory.get(reverse("codes"))
        force_authenticate(request, user=create_user_fixture, token=login_user['output']['access_token'])
        res = CodesView.as_view()(request)
        content = render_response_and_send_content(res)
        assert isinstance(content, dict)
        assert content['status'] == 200
        assert content['output'] == []

    def test_create_icd_code(self, create_icd_code_fixture):
        assert isinstance(create_icd_code_fixture, dict)
        assert create_icd_code_fixture['status'] == 200
        assert isinstance(create_icd_code_fixture['output'], dict)

    def test_get_code(self, create_icd_code_fixture, login_user, create_user_fixture):
        request = factory.get(reverse("code", args=[create_icd_code_fixture['output']['id']]))
        force_authenticate(request, user=create_user_fixture, token=login_user['output']['access_token'])
        res = CodesView.as_view()(request)
        content = render_response_and_send_content(res)
        assert isinstance(content, dict)
        assert content['status'] == 200
        print(content)
        assert isinstance(content['output'], list)

    # def test_delete_code(self, create_icd_code_fixture, login_user, create_user_fixture):
    #     request = factory.delete(reverse("code", args=[create_icd_code_fixture['output']['id']]))
    #     force_authenticate(request, user=create_user_fixture, token=login_user['output']['access_token'])
    #     res = CodesView.as_view()(request)
    #     content = render_response_and_send_content(res)
    #     print(content)

    # def test_update_code(self, create_icd_code_fixture, login_user, create_user_fixture, create_category_fixture):
    #     data = {
    #         "icd_code": "A024",
    #         "description": "Test @",
    #         "icd_code_prefix": "0",
    #         "category": str(create_category_fixture.pk)
    #     }
    #     # request = factory.patch(reverse("code", args=[create_icd_code_fixture['output']['id']]), data=data,
    #     url = f"icd-codes/{create_icd_code_fixture['output']['id']}"
    #     print(f"URL {url}")
    #     request = factory.patch(url, data)
    #     print(f"REQUEST {request}")
    #     force_authenticate(request, user=create_user_fixture, token=login_user['output']['access_token'])
    #     # res = CodesView.as_view()(request)
    #     # content = render_response_and_send_content(res)
    #     # assert isinstance(content, dict)
    #     # assert content['status'] == 200
    #     print("################")
    #     # print(content)
    #     print("#################")
    #     # assert isinstance(content['output'], list)
