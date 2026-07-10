import pytest
from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from apps.listings.models import Listing
from apps.interactions.models import ViewHistory


@pytest.fixture
def listing(db, landlord_user):
    return Listing.objects.create(
        owner=landlord_user,
        title="Test apartment",
        description="Nice apartment in Berlin",
        price=Decimal("1000.00"),
        rooms=2,
        housing_type=Listing.HousingTypes.APARTMENT,
        city="Berlin",
        district="Mitte",
        address="Alexanderplatz 1",
    )


@pytest.mark.django_db
def test_landlord_create_listing(api_client, landlord_user):

    api_client.force_authenticate(user=landlord_user)

    url = reverse("listing-list")

    data = {
        "title": "New apartment",
        "description": "Apartment in Berlin",
        "price": "1200.00",
        "rooms": 3,
        "housing_type": "apartment",
        "city": "Berlin",
        "district": "Mitte",
        "address": "Street 10",
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Listing.objects.count() == 1
    assert Listing.objects.first().owner == landlord_user


@pytest.mark.django_db
def test_tenant_cannot_create_listing(api_client, tenant_user):

    api_client.force_authenticate(user=tenant_user)

    url = reverse("listing-list")

    data = {
        "title": "Apartment",
        "description": "Test",
        "price": "1000.00",
        "rooms": 2,
        "city": "Berlin",
        "address": "Street 1",
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_listing_view_increases_counter(
    authenticated_client,
    listing,
    tenant_user,
):
    url = reverse(
        "listing-detail",
        args=[listing.id]
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    listing.refresh_from_db()

    assert listing.views_count == 1

    assert ViewHistory.objects.filter(
        user=tenant_user,
        listing=listing
    ).exists()


@pytest.mark.django_db
def test_listing_second_view_does_not_duplicate_history(
    authenticated_client,
    listing,
    tenant_user,
):
    url = reverse(
        "listing-detail",
        args=[listing.id]
    )

    authenticated_client.get(url)
    authenticated_client.get(url)

    assert ViewHistory.objects.filter(
        user=tenant_user,
        listing=listing
    ).count() == 1