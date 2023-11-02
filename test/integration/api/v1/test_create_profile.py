"""
Unit tests for ``POST /v1/profile``
"""
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from httpx import Response

from models.profile import Profile
from services.profile import EditProfileRequest, ProfileService


def test_happy_path(client: TestClient, profiles: list[Profile]):
    """
    Creating a profile successfully.
    """
    request_body = EditProfileRequest(
        username="calmcat451",
        password="shortjane",
        gender="female",
        full_name="Ethel Chen",
        street_address="3775 Deerswim Lane",
        email="ethel.chen@example.com",
    )

    expected = {
        "id": 4,
        "username": "calmcat451",
        "password": "shortjane",
        "gender": "female",
        "full_name": "Ethel Chen",
        "street_address": "3775 Deerswim Lane",
        "email": "ethel.chen@example.com",
    }

    response: Response = client.post("/v1/profile", json=jsonable_encoder(request_body))
    assert response.status_code == 200

    # The response contains the new profile details.
    assert response.json() == expected

    # The profile was added to the database.
    assert ProfileService.load_profiles() == [*profiles, Profile(**expected)]
