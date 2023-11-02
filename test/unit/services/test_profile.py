"""
Unit tests for the profile service.
"""

from models.profile import Profile
from services.profile import EditProfileRequest, ProfileService


def test_load_profiles(profiles: list[Profile]):
    """
    Sanity check, to make sure :py:func:ProfileService.load_profiles works as
    expected.

    Note that the ``profiles`` fixture monkey-patches the service to load/save profiles
    in a temporary file.
    """
    loaded_profiles = ProfileService.load_profiles()
    assert loaded_profiles == profiles


def test_save_profiles():
    """
    Sanity check, to make sure :py:func:ProfileService.save_profiles works as
    expected.

    Note that we declared the ``profiles`` fixture as ``autouse=True``, so it will
    run for this test even though we didn't include it in the test function parameters.
    """
    new_profiles = [
        Profile(
            id=1,
            username="orangelion962",
            password="1952",
            gender="male",
            full_name="Arlo Edwards",
            street_address="4717 Flaxmere Ave",
            email="arlo.edwards@example.com",
        ),
        Profile(
            id=2,
            username="organicwolf415",
            password="julius",
            gender="female",
            full_name="Lily Wright",
            street_address="6203 Hillsborough Road",
            email="lily.wright@example.com",
        ),
    ]

    ProfileService.save_profiles(new_profiles)

    loaded_profiles = ProfileService.load_profiles()
    assert loaded_profiles == new_profiles


def test_get_profile_by_id_happy_path(profiles: list[Profile]):
    """
    Getting a profile by its ID.
    """
    assert ProfileService.get_profile_by_id(profiles[0].id) == profiles[0]


def test_get_profile_by_id_non_existent():
    """
    Attempting to get a profile that doesn't exist.
    """
    assert ProfileService.get_profile_by_id(999) is None


def test_edit_profile_by_id_happy_path(profiles: list[Profile]):
    """
    Editing a profile by its ID.
    """
    target_profile = profiles[0]

    data = EditProfileRequest(
        username="calmcat451",
        password="shortjane",
        gender="female",
        full_name="Ethel Chen",
        street_address="3775 Deerswim Lane",
        email="ethel.chen@example.com",
    )

    actual: Profile = ProfileService.edit_profile_by_id(target_profile.id, data)

    # ID cannot be edited.
    assert actual.id == target_profile.id

    assert actual.username == data.username
    assert actual.password == data.password
    assert actual.gender == data.gender
    assert actual.full_name == data.full_name
    assert actual.street_address == data.street_address
    assert actual.email == data.email

    # Verify that the saved profile was correctly stored in the "database".
    loaded_profiles = ProfileService.load_profiles()

    # Non-matching profiles were saved unmodified.
    assert loaded_profiles[1:] == profiles[1:]

    # The updated profile was saved correctly.
    assert dict(loaded_profiles[0]) == {
        "id": target_profile.id,
        "username": "calmcat451",
        "password": "shortjane",
        "gender": "female",
        "full_name": "Ethel Chen",
        "street_address": "3775 Deerswim Lane",
        "email": "ethel.chen@example.com",
    }


def test_edit_profile_by_id_non_existent(profiles: list[Profile]):
    """
    Attempting to edit a profile that doesn't exist.
    """
    data = EditProfileRequest(
        username="calmcat451",
        password="shortjane",
        gender="female",
        full_name="Ethel Chen",
        street_address="3775 Deerswim Lane",
        email="ethel.chen@example.com",
    )

    assert ProfileService.edit_profile_by_id(999, data) is None

    # No changes were made to the "database".
    assert ProfileService.load_profiles() == profiles


def test_create_profile_happy_path(profiles: list[Profile]):
    """
    Successfully adding a profile to the database.
    """
    data = EditProfileRequest(
        username="calmcat451",
        password="shortjane",
        gender="female",
        full_name="Ethel Chen",
        street_address="3775 Deerswim Lane",
        email="ethel.chen@example.com",
    )

    expected = Profile(
        id=4,
        username="calmcat451",
        password="shortjane",
        gender="female",
        full_name="Ethel Chen",
        street_address="3775 Deerswim Lane",
        email="ethel.chen@example.com",
    )

    actual: Profile = ProfileService.create_profile(data)

    # The new profile is returned.
    assert actual == expected

    # The new profile was added to the "database".
    assert ProfileService.load_profiles() == [*profiles, expected]
