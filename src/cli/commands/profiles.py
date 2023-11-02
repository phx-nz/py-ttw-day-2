__all__ = ["app"]

import orjson
import typer
from fastapi.encoders import jsonable_encoder

from models.profile import Profile
from services.profile import EditProfileRequest, ProfileService

app = typer.Typer(name="profiles")


@app.command("get")
def get_profile(profile_id: int):
    """
    Retrieves the profile with the specified ID and outputs the details in JSON format.

    :raises: ValueError if no such profile exists.
    """
    # Find the profile with the matching ID.
    # We can leverage what we wrote during yesterday's exercise.  Reusability FTW!
    profile: Profile = ProfileService.get_profile_by_id(profile_id)

    if not profile:
        raise ValueError(f"No profile exists with ID {profile_id}")

    output_profile(profile)


@app.command("update")
def update_profile(profile_id: int, data_filepath: str):
    """
    Updates the profile with the specified ID, using the data at the specified
    filepath.

    Outputs the updated profile data on success.

    :raises: ValueError if no such profile exists.
    :raises: pydantic.ValidationError if the data are malformed.
    """
    with open(data_filepath, "rb") as f:
        data = EditProfileRequest(**orjson.loads(f.read()))

    updated_profile: Profile = ProfileService.edit_profile_by_id(profile_id, data)

    if not updated_profile:
        raise ValueError(f"No profile exists with ID {profile_id}")

    output_profile(updated_profile)


@app.command("create")
def create_profile(data_filepath: str):
    """
    Creates a new profile, using the data at the specified filepath.

    Outputs the new profile data on success.

    :raises: pydantic.ValidationError if the data are malformed.
    """
    with open(data_filepath, "rb") as f:
        data = EditProfileRequest(**orjson.loads(f.read()))

    new_profile: Profile = ProfileService.create_profile(data)

    output_profile(new_profile)


def output_profile(profile: Profile) -> None:
    """
    Outputs profile data to stdout.
    """
    # Convert the model instance into a value that can be JSON-encoded.
    encoded_profile = jsonable_encoder(profile)

    # Finally, output the value in JSON format.
    # Note that :py:func:`orjson.dumps` returns a binary string, so we have to decode
    # it.
    print(orjson.dumps(encoded_profile, option=orjson.OPT_INDENT_2).decode("utf-8"))
