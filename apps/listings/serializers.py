from rest_framework import serializers

from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Listing
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "price",
            "rooms",
            "housing_type",
            "city",
            "district",
            "address",
            "is_active",
            "views_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "owner",
            "views_count",
            "created_at",
            "updated_at",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Цена должна быть больше 0."
            )
        return value

    def validate_rooms(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Количество комнат должно быть не меньше 1."
            )
        return value