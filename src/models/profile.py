"""
User profile model definition.
"""
from datetime import datetime

from pydantic import BaseModel


class Profile(BaseModel):
    """
    Information about a user, so that we can personalise the API experience for them.
    """

    id: int
    username: str
    password: str
    gender: str
    full_name: str
    street_address: str
    email: str
    created_at: datetime
