from rest_framework import serializers

from .models import Booking

from django.db.models import Q


class BookingSerializer(serializers.ModelSerializer):

    tenant_email = serializers.ReadOnlyField(
        source="tenant.email"
    )

    listing_title = serializers.ReadOnlyField(
        source="listing.title"
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "tenant",
            "tenant_email",
            "listing",
            "listing_title",
            "start_date",
            "end_date",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "tenant",
            "status",
            "created_at",
        ]

    def validate(self, attrs):

        # Если это PATCH/PUT существующей брони —
        # пропускаем проверки создания
        if self.instance:
            return attrs

        listing = attrs.get("listing")

        if listing is None:
            raise serializers.ValidationError(
                "Необходимо указать объявление."
            )

        if not listing.is_active:
            raise serializers.ValidationError(
                "Это объявление недоступно."
            )

        if listing.owner == self.context["request"].user:
            raise serializers.ValidationError(
                "Нельзя забронировать собственное объявление."
            )

        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        active_bookings = Booking.objects.filter(
            listing=listing,
            status__in=["pending", "confirmed"],
            start_date__lt=end_date,
            end_date__gt=start_date,
        )

        if active_bookings.exists():
            raise serializers.ValidationError(
                "На эти даты уже существует активная бронь."
            )

        return attrs