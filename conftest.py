import pytest
from rest_framework.test import APIClient
from courses_online.courses_online_apps.users.models import BaseUser

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user = BaseUser.objects.create_user(
        email="test@test.com",
        password="test123",
        phone="123456789"
    )
    user.set_password("test123")
    user.save()
    return user

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client