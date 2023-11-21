"""
Define routes for our v1 API.
"""
__all__ = ["router"]

from fastapi import APIRouter, HTTPException

from models.profile import Profile
from services.profile import EditProfileRequest, ProfileService

# All API routes defined in this module will have a path prefix of ``/v1``.
# E.g., ``@router.get("/foo/bar")`` adds a route at ``/v1/foo/bar``.
# :see: https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
router = APIRouter(prefix="/v1", tags=["v1"])


@router.get("/")
def index() -> dict:
    """
    Simple static route, so that we can confirm the server is running.
    """
    return {"message": "Kia ora te ao!"}


@router.get("/profile/{profile_id}")
def get_profile(profile_id: int) -> Profile:
    """
    Retrieves the profile with the specified ID.

    Returns a 404 if no such profile exists.
    """
    profile = ProfileService.get_profile_by_id(profile_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("/profile/{profile_id}")
def edit_profile(profile_id: int, body: EditProfileRequest) -> Profile:
    """
    Edits the profile with the specified ID, replacing its attributes from the request
    body, and returns the modified profile.

    Returns a 404 if no such profile exists.
    """
    profile = ProfileService.edit_profile_by_id(profile_id, body)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.post("/profile")
def create_profile(body: EditProfileRequest) -> Profile:
    """
    Adds a profile to the database using the attributes from the response body, and
    returns the new profile data.
    """
    return ProfileService.create_profile(body)
