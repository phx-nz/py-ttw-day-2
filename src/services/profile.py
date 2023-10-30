"""
Use cases for working with profiles.
"""
__all__ = [
    "edit_profile_by_id",
    "get_profile_by_id",
    "load_profiles",
    "save_profiles",
]

from pathlib import Path

import orjson
from pydantic import BaseModel

from models.profile import Profile


def _get_data_file() -> Path:
    """
    Returns the path to the file where profiles are stored.

    Written as its own function so that we can mock it during unit tests.
    """
    # src/data/profiles.json
    return Path(__file__).parent.parent / "data" / "profiles.json"


def _find_profile_by_id(profile_id: int, profiles: list[Profile]) -> Profile | None:
    """
    Finds the profile with the specified ID, or ``None`` if no such profile exists.
    """
    try:
        # Iterate through ``profiles`` until we find the first one with matching ID.
        return next(p for p in profiles if p.id == profile_id)
    except StopIteration:
        # The generator will raise ``StopIteration`` if it reaches the end of the list
        # without finding a match.
        return None


def get_profile_by_id(profile_id: int) -> Profile | None:
    """
    Returns the profile with the specified ID, or ``None`` if no such profile exists.
    """
    return _find_profile_by_id(profile_id, load_profiles())


class EditProfileRequest(BaseModel):
    """
    DTO for passing updated profile data to :py:func:`edit_profile_by_id`.
    """

    username: str
    password: str
    gender: str
    full_name: str
    street_address: str
    email: str


def edit_profile_by_id(profile_id: int, data: EditProfileRequest) -> Profile | None:
    """
    Modifies the profile with the specified ID, replacing its attributes from ``data``.

    Returns the modified profile on success, or ``None`` if no such profile exists.
    """
    profiles = load_profiles()
    target_profile = _find_profile_by_id(profile_id, profiles)

    if not target_profile:
        return None

    # Create a copy of the profile with the modified attributes.
    # See https://github.com/pydantic/pydantic/discussions/3139 for other approaches.
    target_profile = Profile(**(dict(target_profile) | dict(data)))

    # Save the list of profiles, substituting the modified profile in place of the
    # original.
    save_profiles([target_profile if p.id == profile_id else p for p in profiles])

    return target_profile


def load_profiles() -> list[Profile]:
    """
    Loads profiles from the data file.

    Note that this function is synchronous, which is not ideal for I/O operations.  It's
    OK for now because we'll replace all of this with a proper database tomorrow (:
    """
    with open(_get_data_file(), "rb") as f:
        return [Profile(**record) for record in orjson.loads(f.read())]


def save_profiles(profiles: list[Profile]) -> None:
    """
    Saves profiles to the data file, replacing anything that's currently there.

    Note that this function is synchronous, which is not ideal for I/O operations.  It's
    OK for now because we'll replace all of this with a proper database tomorrow (:
    """
    with open(_get_data_file(), "wb") as f:
        f.write(orjson.dumps(list(map(dict, profiles)), option=orjson.OPT_INDENT_2))
