import pytest
from rest_framework.test import APIClient
from courses_online.courses_online_apps.users.models import BaseUser


@pytest.mark.django_db
def test_register_user_success():
    client = APIClient()
    data = {"email": "alex@gmail.com", "password": "123", "username": "tester"}

    response = client.post("/api/users/register/", data)

    assert response.status_code == 201
    assert BaseUser.objects.filter(email="alex@gmail.com").exists()