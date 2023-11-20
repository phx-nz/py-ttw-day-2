__all__ = ["EditProfileRequest", "ProfileService"]

from pathlib import Path

import orjson
from pydantic import BaseModel, Field

from models.profile import Profile


class EditProfileRequest(BaseModel):
    """
    DTO for passing updated profile to :py:func:`ProfileService.edit_profile_by_id`.
    """

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    gender: str
    full_name: str = Field(min_length=1)
    street_address: str = Field(min_length=1)
    email: str = Field(min_length=1, pattern=r"@")


class ProfileService:
    """
    Use cases for working with profiles.
    """

    @staticmethod
    def get_profile_by_id(profile_id: int) -> Profile | None:
        """
        Returns the profile with the specified ID, or ``None`` if no such profile exists.
        """
        return ProfileService._find_profile_by_id(
            profile_id, ProfileService.load_profiles()
        )

    @staticmethod
    def edit_profile_by_id(profile_id: int, data: EditProfileRequest) -> Profile | None:
        """
        Modifies the profile with the specified ID, replacing its attributes from ``data``.

        Returns the modified profile on success, or ``None`` if no such profile exists.
        """
        profiles = ProfileService.load_profiles()
        target_profile = ProfileService._find_profile_by_id(profile_id, profiles)

        if not target_profile:
            return None

        # Create a copy of the profile with the modified attributes.
        # See https://github.com/pydantic/pydantic/discussions/3139 for other approaches.
        target_profile = Profile(**(dict(target_profile) | dict(data)))

        # Save the list of profiles, substituting the modified profile in place of the
        # original.
        ProfileService.save_profiles(
            [target_profile if p.id == profile_id else p for p in profiles]
        )

        return target_profile

    @staticmethod
    def create_profile(data: EditProfileRequest) -> Profile:
        """
        Adds a new profile to the database and returns it.
        """
        profiles = ProfileService.load_profiles()

        new_id = max(p.id for p in profiles) + 1
        new_profile = Profile(id=new_id, **dict(data))

        ProfileService.save_profiles([*profiles, new_profile])

        return new_profile

    @staticmethod
    def _find_profile_by_id(profile_id: int, profiles: list[Profile]) -> Profile | None:
        """
        Finds the profile with the specified ID, or ``None`` if no such profile exists.
        """
        try:
            # Iterate through ``profiles`` until we find the first one with matching ID.
            return next(p for p in profiles if p.id == profile_id)
        except StopIteration:
            # The generator will raise ``StopIteration`` if it reaches the end of the
            # list without finding a match.
            return None

    @staticmethod
    def load_profiles() -> list[Profile]:
        """
        Loads profiles from the data file.
        Note that this function is synchronous, which is not ideal for I/O operations.
        It's OK for now because we'll replace it with a proper database tomorrow (:
        """
        with open(ProfileService._get_data_file(), "rb") as f:
            return [Profile(**record) for record in orjson.loads(f.read())]

    @staticmethod
    def save_profiles(profiles: list[Profile]) -> None:
        """
        Saves profiles to the data file, replacing anything that's currently there.

        Note that this function is synchronous, which is not ideal for I/O operations.
        It's OK for now because we'll replace it with a proper database tomorrow (:
        """
        with open(ProfileService._get_data_file(), "wb") as f:
            f.write(orjson.dumps(list(map(dict, profiles)), option=orjson.OPT_INDENT_2))

    @staticmethod
    def _get_data_file() -> Path:
        """
        Returns the path to the file where profiles are stored.

        Written as its own function so that we can mock it during unit tests.
        """
        # src/data/profiles.json
        return Path(__file__).parent.parent / "data" / "profiles.json"
