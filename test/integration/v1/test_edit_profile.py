"""
Unit tests for PUT ``/v1/profile/{profile_id}``.
"""
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from models.profile import Profile
from services.profile import EditProfileRequest


def test_happy_path(client: TestClient, profiles: list[Profile]):
    """
    Editing a profile successfully.
    """
    target_profile = profiles[0]

    request_body = EditProfileRequest(
        username="calmcat451",
        password="shortjane",
        gender="female",
        full_name="Ethel Chen",
        street_address="3775 Deerswim Lane",
        email="ethel.chen@example.com",
    )

    response = client.put(
        f"/v1/profile/{target_profile.id}",
        json=dict(request_body),
    )

    assert response.status_code == 200

    # The response will contain the profile data, with updated values.
    expected_response = jsonable_encoder(target_profile)
    expected_response.update(request_body)

    assert response.json() == expected_response


def test_non_existent_profile(client: TestClient):
    """
    Attempting to edit a nonexistent profile.
    """
    request_body = EditProfileRequest(
        username="calmcat451",
        password="shortjane",
        gender="female",
        full_name="Ethel Chen",
        street_address="3775 Deerswim Lane",
        email="ethel.chen@example.com",
    )

    response = client.put("/v1/profile/999", json=dict(request_body))
    assert response.status_code == 404
