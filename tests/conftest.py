import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.listings.models import Listing
from apps.bookings.models import Booking

from decimal import Decimal
from datetime import date, timedelta


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def tenant_user(db):
    return User.objects.create_user(
        username="tenant_test",
        email="tenant@test.com",
        password="testpassword123",
        role=User.Roles.TENANT,
    )


@pytest.fixture
def landlord_user(db):
    return User.objects.create_user(
        username="landlord_test",
        email="landlord@test.com",
        password="testpassword123",
        role=User.Roles.LANDLORD,
    )


@pytest.fixture
def authenticated_client(api_client, tenant_user):
    api_client.force_authenticate(
        user=tenant_user
    )
    return api_client

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

@pytest.fixture
def listing(db, landlord_user):
    return Listing.objects.create(
        owner=landlord_user,
        title="Test apartment",
        description="Nice apartment",
        price="1000.00",
        rooms=2,
        housing_type=Listing.HousingTypes.APARTMENT,
        city="Berlin",
        district="Mitte",
        address="Alexanderplatz 1",
    )


@pytest.fixture
def booking(db, tenant_user, listing):
    return Booking.objects.create(
        tenant=tenant_user,
        listing=listing,
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=5),
    )