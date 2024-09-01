from pydantic import BaseModel, Field


class LoginUserInputDto(BaseModel):
    email: str = Field(..., example="example@fake.com")
    password: str = Field(..., example="password")
