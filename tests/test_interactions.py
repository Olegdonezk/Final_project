import pytest

from apps.interactions.models import SearchHistory, ViewHistory


@pytest.mark.django_db
def test_search_history_list(
    authenticated_client,
    tenant_user,
):
    SearchHistory.objects.create(
        user=tenant_user,
        query_text="Berlin",
    )

    SearchHistory.objects.create(
        user=tenant_user,
        query_text="Apartment",
    )

    response = authenticated_client.get("/api/interactions/searches/")

    assert response.status_code == 200
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2

@pytest.mark.django_db
def test_view_history_list(
    authenticated_client,
    tenant_user,
    listing,
):
    ViewHistory.objects.create(
        user=tenant_user,
        listing=listing,
    )

    response = authenticated_client.get("/api/interactions/views/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1

@pytest.mark.django_db
def test_popular_searches(
    authenticated_client,
    tenant_user,
):
    SearchHistory.objects.create(
        user=tenant_user,
        query_text="Berlin",
    )

    SearchHistory.objects.create(
        user=tenant_user,
        query_text="Berlin",
    )

    SearchHistory.objects.create(
        user=tenant_user,
        query_text="Apartment",
    )

    response = authenticated_client.get(
        "/api/interactions/popular-searches/"
    )

    assert response.status_code == 200

    assert response.data[0]["query_text"] == "Berlin"
    assert response.data[0]["search_count"] == 2

    assert response.data[1]["query_text"] == "Apartment"
    assert response.data[1]["search_count"] == 1