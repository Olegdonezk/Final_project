from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .permissions import IsReviewOwnerOrReadOnly

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsReviewOwnerOrReadOnly,
    ]

    def get_queryset(self):
        return Review.objects.select_related(
            "booking",
            "booking__tenant",
            "booking__listing"
        )

    def perform_create(self, serializer):

        booking = serializer.validated_data.get("booking")

        if not booking:
            raise PermissionDenied(
                "Необходимо указать бронирование."
            )

        if booking.tenant != self.request.user:
            raise PermissionDenied(
                "Можно оставлять отзыв только после своей аренды."
            )

        serializer.save()