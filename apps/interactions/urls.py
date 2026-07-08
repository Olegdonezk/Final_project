from rest_framework.routers import DefaultRouter

from .views import (
    SearchHistoryViewSet,
    ViewHistoryViewSet,
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