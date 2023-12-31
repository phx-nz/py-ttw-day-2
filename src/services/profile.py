__all__ = ["ProfileService"]

from pathlib import Path

import orjson

from models.profile import Profile


class ProfileService:
    """
    Use cases for working with profiles.
    """

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
