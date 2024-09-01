from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TokenInputModel(BaseModel):
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None
    roles: List[str] = []
    sub: str
    email: str
    host: Optional[str] = None
