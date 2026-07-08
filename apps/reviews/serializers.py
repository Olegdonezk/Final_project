from rest_framework import serializers

from .models import Review
from apps.bookings.models import Booking


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review

        fields = [
            "id",
            "user",
            "listing",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]


    def validate(self, attrs):

        request = self.context["request"]

        listing = attrs.get("listing")


        # Проверяем, была ли завершённая бронь
        has_completed_booking = Booking.objects.filter(
            tenant=request.user,
            listing=listing,
            status=Booking.Status.COMPLETED
        ).exists()


        if not has_completed_booking:
            raise serializers.ValidationError(
                "Оставить отзыв можно только после завершённой брони."
            )


        # Проверяем, нет ли уже отзыва
        already_exists = Review.objects.filter(
            user=request.user,
            listing=listing
        ).exists()


        if already_exists:
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на это объявление."
            )


        return attrs


    def create(self, validated_data):

        validated_data["user"] = self.context["request"].user

        return super().create(validated_data)