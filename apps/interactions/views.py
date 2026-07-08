from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import SearchHistory, ViewHistory
from .serializers import (
    SearchHistorySerializer,
    ViewHistorySerializer,
)


class SearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(
            user=self.request.user
        )


class ViewHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ViewHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ViewHistory.objects.filter(
            user=self.request.user
        )