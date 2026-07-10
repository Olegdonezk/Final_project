from rest_framework.routers import DefaultRouter

from django.urls import path

from .views import (
    SearchHistoryViewSet,
    ViewHistoryViewSet,
    PopularSearchesView,
)

router = DefaultRouter()

router.register(
    "searches",
    SearchHistoryViewSet,
    basename="search-history",
)

router.register(
    "views",
    ViewHistoryViewSet,
    basename="view-history",
)

urlpatterns = router.urls

urlpatterns += [
    path(
        "popular-searches/",
        PopularSearchesView.as_view(),
        name="popular-searches",
    ),
]