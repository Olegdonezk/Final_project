from rest_framework import serializers

from .models import Review
from apps.bookings.models import Booking


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review

        fields = [
            "id",
            "booking",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_booking(self, booking):
        request = self.context["request"]

        if booking.tenant != request.user:
            raise serializers.ValidationError(
                "Вы можете оставить отзыв только на свою бронь."
            )

        if booking.status != Booking.Status.COMPLETED:
            raise serializers.ValidationError(
                "Оставить отзыв можно только после завершения брони."
            )

        if hasattr(booking, "review"):
            raise serializers.ValidationError(
                "Для этой брони уже существует отзыв."
            )

        return booking