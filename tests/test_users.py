import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_register_user(api_client):

    url = reverse("register")

    data = {
        "username": "new_user",
        "email": "new@test.com",
        "password": "password123",
        "role": "tenant",
    }

    response = api_client.post(
        url,
        data
    )

    assert response.status_code == 201
    assert response.data["email"] == "new@test.com"


@pytest.mark.django_db
def test_profile_authenticated(
    authenticated_client,
    tenant_user
):

    url = reverse("profile")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == tenant_user.email