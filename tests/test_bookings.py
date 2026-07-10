import pytest

from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status

from apps.bookings.models import Booking


@pytest.mark.django_db
def test_tenant_create_booking(
    api_client,
    tenant_user,
    listing,
):
    api_client.force_authenticate(user=tenant_user)

    url = reverse("bookings-list")

    data = {
        "listing": listing.id,
        "start_date": str(date.today() + timedelta(days=10)),
        "end_date": str(date.today() + timedelta(days=15)),
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Booking.objects.count() == 1

@pytest.mark.django_db
def test_landlord_cannot_book_own_listing(
    api_client,
    landlord_user,
    listing,
):
    api_client.force_authenticate(user=landlord_user)

    url = reverse("bookings-list")

    data = {
        "listing": listing.id,
        "start_date": str(date.today() + timedelta(days=10)),
        "end_date": str(date.today() + timedelta(days=15)),
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_tenant_cancel_booking(
    authenticated_client,
    booking,
):
    url = reverse(
        "bookings-cancel",
        args=[booking.id],
    )

    response = authenticated_client.patch(url)

    assert response.status_code == status.HTTP_200_OK

    booking.refresh_from_db()

    assert booking.status == Booking.Status.CANCELLED

@pytest.mark.django_db
def test_landlord_confirm_booking(
    api_client,
    landlord_user,
    booking,
):
    api_client.force_authenticate(user=landlord_user)

    url = reverse(
        "bookings-confirm",
        args=[booking.id],
    )

    response = api_client.patch(url)

    assert response.status_code == status.HTTP_200_OK

    booking.refresh_from_db()

    assert booking.status == Booking.Status.CONFIRMED

@pytest.mark.django_db
def test_landlord_complete_booking(
    api_client,
    landlord_user,
    booking,
):
    booking.status = Booking.Status.CONFIRMED
    booking.save()

    api_client.force_authenticate(user=landlord_user)

    url = reverse(
        "bookings-complete",
        args=[booking.id],
    )

    response = api_client.patch(url)

    assert response.status_code == status.HTTP_200_OK

    booking.refresh_from_db()

    assert booking.status == Booking.Status.COMPLETED