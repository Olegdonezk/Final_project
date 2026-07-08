from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from .models import Listing
from .serializers import ListingSerializer
from .filters import ListingFilter

from django.db.models import F

from apps.interactions.models import ViewHistory, SearchHistory




class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # Фильтрация
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ListingFilter

    # Поиск
    search_fields = [
        "title",
        "description",
        "city",
        "district",
        "address",
    ]

    # Сортировка
    ordering_fields = [
        "price",
        "created_at",
        "rooms",
        "views_count",
    ]

    ordering = ["-created_at"]

    def perform_create(self, serializer):
        if self.request.user.role != "landlord":
            raise PermissionDenied(
                "Только арендодатель может создавать объявления."
            )
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()

        # Увеличиваем количество просмотров
        Listing.objects.filter(pk=listing.pk).update(
            views_count=F("views_count") + 1
        )

        listing.refresh_from_db()

        # Сохраняем историю просмотра только для авторизованных пользователей
        if request.user.is_authenticated:
            ViewHistory.objects.create(
                user=request.user,
                listing=listing
            )

        serializer = self.get_serializer(listing)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):

        search_query = request.query_params.get("search")

        if (
                request.user.is_authenticated
                and search_query
        ):
            SearchHistory.objects.create(
                user=request.user,
                query_text=search_query
            )

        return super().list(request, *args, **kwargs)