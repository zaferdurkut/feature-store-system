from typing import List, Optional

from pydantic import BaseModel, Field


class LoginOutputDto(BaseModel):
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
