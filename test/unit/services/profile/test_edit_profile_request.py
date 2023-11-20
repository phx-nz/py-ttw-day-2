import pytest
from pydantic import ValidationError

from services.profile import EditProfileRequest


def test_invalid_username_empty():
    """
    Attempting to set a profile's username to an empty string.
    """
    with pytest.raises(ValidationError):
        EditProfileRequest(
            username="",
            password="shortjane",
            gender="female",
            full_name="Ethel Chen",
            street_address="3775 Deerswim Lane",
            email="ethel.chen@example.com",
        )


def test_invalid_password_empty():
    """
    Attempting to set a profile's password to an empty string.
    """
    with pytest.raises(ValidationError):
        EditProfileRequest(
            username="calmcat451",
            password="",
            gender="female",
            full_name="Ethel Chen",
            street_address="3775 Deerswim Lane",
            email="ethel.chen@example.com",
        )


def test_invalid_full_name_empty():
    """
    Attempting to set a profile's full name to an empty string.
    """
    with pytest.raises(ValidationError):
        EditProfileRequest(
            username="calmcat451",
            password="shortjane",
            gender="female",
            full_name="",
            street_address="3775 Deerswim Lane",
            email="ethel.chen@example.com",
        )


def test_invalid_street_address_empty():
    """
    Attempting to set a profile's street address to an empty string.
    """
    with pytest.raises(ValidationError):
        EditProfileRequest(
            username="calmcat451",
            password="shortjane",
            gender="female",
            full_name="Ethel Chen",
            street_address="",
            email="ethel.chen@example.com",
        )


def test_invalid_email_empty():
    """
    Attempting to set a profile's email address to an empty string.
    """
    with pytest.raises(ValidationError):
        EditProfileRequest(
            username="calmcat451",
            password="shortjane",
            gender="female",
            full_name="Ethel Chen",
            street_address="3775 Deerswim Lane",
            email="",
        )


def test_invalid_email_missing_at_symbol():
    """
    The profile's email address must contain a ``@`` symbol.
    """
    with pytest.raises(ValidationError):
        EditProfileRequest(
            username="calmcat451",
            password="shortjane",
            gender="female",
            full_name="Ethel Chen",
            street_address="3775 Deerswim Lane",
            email="ethel.chen",
        )
