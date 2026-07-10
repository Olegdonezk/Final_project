import pytest

from django.urls import reverse
from rest_framework import status

from apps.bookings.models import Booking
from apps.reviews.models import Review


@pytest.fixture
def completed_booking(booking):
    booking.status = Booking.Status.COMPLETED
    booking.save()
    return booking


@pytest.mark.django_db
def test_create_review(
    authenticated_client,
    completed_booking,
):
    url = reverse("reviews-list")

    data = {
        "booking": completed_booking.id,
        "rating": 5,
        "comment": "Excellent apartment!",
    }

    response = authenticated_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    assert Review.objects.count() == 1

    review = Review.objects.first()

    assert review.booking == completed_booking
    assert review.rating == 5


@pytest.mark.django_db
def test_cannot_review_uncompleted_booking(
    authenticated_client,
    booking,
):
    url = reverse("reviews-list")

    data = {
        "booking": booking.id,
        "rating": 5,
        "comment": "Excellent apartment!",
    }

    response = authenticated_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_cannot_create_second_review(
    authenticated_client,
    completed_booking,
):
    Review.objects.create(
        booking=completed_booking,
        rating=5,
        comment="First review",
    )

    url = reverse("reviews-list")

    data = {
        "booking": completed_booking.id,
        "rating": 4,
        "comment": "Second review",
    }

    response = authenticated_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_user_cannot_review_another_users_booking(
    api_client,
    landlord_user,
    completed_booking,
):
    api_client.force_authenticate(user=landlord_user)

    url = reverse("reviews-list")

    data = {
        "booking": completed_booking.id,
        "rating": 5,
        "comment": "Great!",
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Review.objects.count() == 0