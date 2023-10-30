"""
Unit tests for GET ``/v1/profile/<profile_id>``.
"""
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from models.profile import Profile


def test_happy_path(client: TestClient, profiles: list[Profile]):
    """
    Requesting a valid profile ID.
    """
    target_profile = profiles[0]

    response = client.get(f"/v1/profile/{target_profile.id}")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(target_profile)


def test_non_existent_profile(client: TestClient):
    """
    Requesting a nonexistent profile ID.
    """
    response = client.get("/v1/profile/999")
    assert response.status_code == 404
