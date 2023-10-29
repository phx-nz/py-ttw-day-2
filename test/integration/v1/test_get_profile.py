"""
Unit tests for GET ``/v1/profile/<profile_id>``.
"""
from fastapi.testclient import TestClient

from models.profile import Profile


def test_happy_path(client: TestClient, profiles: list[Profile]):
    """
    Requesting a valid profile ID.
    """
    target_profile = profiles[0]

    response = client.get(f"/v1/profile/{target_profile.id}")
    assert response.status_code == 200

    # Created date is a ``datetime``, which gets converted to a string when FastAPI
    # JSON-encodes the response body.
    expected_response = dict(target_profile)
    expected_response["created_at"] = expected_response["created_at"].isoformat()

    assert response.json() == expected_response


def test_non_existent_profile(client: TestClient):
    """
    Requesting a nonexistent profile ID.
    """
    response = client.get("/v1/profile/999")
    assert response.status_code == 404
