from pydantic import BaseModel


class LoginOutputModel(BaseModel):
    access_token: str
    refresh_token: str
