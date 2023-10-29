"""
Unit tests for the profile service.
"""
from datetime import datetime

from models.profile import Profile
from services import profile as my_service
from services.profile import EditProfileRequest


def test_load_profiles(profiles: list[Profile]):
    """
    Sanity check, to make sure :py:func:my_service.load_profiles works as
    expected.

    Note that the ``profiles`` fixture monkey-patches the service to load/save profiles
    in a temporary file.
    """
    loaded_profiles = my_service.load_profiles()
    assert loaded_profiles == profiles


def test_save_profiles():
    """
    Sanity check, to make sure :py:func:my_service.save_profiles works as
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
            created_at=datetime(2013, 6, 30, 5, 36, 41, 256000),
        ),
        Profile(
            id=2,
            username="organicwolf415",
            password="julius",
            gender="female",
            full_name="Lily Wright",
            street_address="6203 Hillsborough Road",
            email="lily.wright@example.com",
            created_at=datetime(2019, 10, 30, 13, 38, 54, 248000),
        ),
    ]

    my_service.save_profiles(new_profiles)

    loaded_profiles = my_service.load_profiles()
    assert loaded_profiles == new_profiles


def test_get_profile_by_id_happy_path(profiles: list[Profile]):
    """
    Getting a profile by its ID.
    """
    assert my_service.get_profile_by_id(profiles[0].id) == profiles[0]


def test_get_profile_by_id_non_existent():
    """
    Attempting to get a profile that doesn't exist.
    """
    assert my_service.get_profile_by_id(999) is None


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

    actual: Profile = my_service.edit_profile_by_id(target_profile.id, data)

    assert actual.username == data.username
    assert actual.password == data.password
    assert actual.gender == data.gender
    assert actual.full_name == data.full_name
    assert actual.street_address == data.street_address
    assert actual.email == data.email

    # These attributes cannot be edited.
    assert actual.id == target_profile.id
    assert actual.created_at == target_profile.created_at

    # Verify that the saved profile was correctly stored in the "database".
    loaded_profiles = my_service.load_profiles()

    # Non-matching profiles were saved unmodified.
    assert loaded_profiles[1:] == profiles[1:]

    # The updated profile was saved correctly.
    assert loaded_profiles[0].username == data.username
    assert loaded_profiles[0].password == data.password
    assert loaded_profiles[0].gender == data.gender
    assert loaded_profiles[0].full_name == data.full_name
    assert loaded_profiles[0].street_address == data.street_address
    assert loaded_profiles[0].email == data.email
    assert loaded_profiles[0].id == target_profile.id
    assert loaded_profiles[0].created_at == target_profile.created_at


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

    assert my_service.edit_profile_by_id(999, data) is None

    # No changes were made to the "database".
    assert my_service.load_profiles() == profiles
