from rest_framework import serializers

from .models import SearchHistory, ViewHistory


class SearchHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchHistory
        fields = "__all__"
        read_only_fields = [
            "user",
            "searched_at",
        ]


class ViewHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ViewHistory
        fields = "__all__"
        read_only_fields = [
            "user",
            "viewed_at",
        ]