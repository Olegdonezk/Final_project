from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        return Review.objects.select_related(
            "booking",
            "booking__tenant",
            "booking__listing"
        )

    def perform_create(self, serializer):
        serializer.save()