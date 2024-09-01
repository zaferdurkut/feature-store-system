from typing import List, Optional

from pydantic import BaseModel, Field


class LoginUserInputModel(BaseModel):
    email: str
    password: str
