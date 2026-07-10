from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count


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

class PopularSearchesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        popular = (
            SearchHistory.objects
            .exclude(query_text="")
            .values("query_text")
            .annotate(search_count=Count("id"))
            .order_by("-search_count")[:10]
        )

        return Response(popular)