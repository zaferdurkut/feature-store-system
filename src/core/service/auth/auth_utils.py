import random
import string
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from src.core.model.auth.token_output_model import TokenOutputModel
from src.infra.config.logging_config import get_logger

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
AUTH_ALGORITHM = "HS256"
JWT_SECRET_KEY = "dummy_secret_key" # TODO: Change this to a more secure secret key


logger = get_logger()


class AuthUtils:
    def __init__(
        self,
    ):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.JWT_SECRET_KEY = JWT_SECRET_KEY

    def get_hashed_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)

    def create_access_token(
        self,
        token_output_model=TokenOutputModel,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        timestamp_utc = datetime.utcnow()
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta

        else:
            expires_delta = timestamp_utc + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )

        token_output_model.exp = expires_delta
        token_output_model.iat = timestamp_utc

        encoded_jwt = jwt.encode(
            token_output_model.model_dump(), self.JWT_SECRET_KEY, AUTH_ALGORITHM
        )

        return encoded_jwt

    def create_refresh_token(
        self,
        token_output_model=TokenOutputModel,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        timestamp_utc = datetime.utcnow()
        if expires_delta is not None:
            expires_delta = timestamp_utc + expires_delta
        else:
            expires_delta = timestamp_utc + timedelta(
                minutes=REFRESH_TOKEN_EXPIRE_MINUTES
            )

        token_output_model.exp = expires_delta
        token_output_model.iat = timestamp_utc

        encoded_jwt = jwt.encode(
            token_output_model.model_dump(), self.JWT_SECRET_KEY, AUTH_ALGORITHM
        )
        return encoded_jwt

    def generate_confirmation_code(
        self,
        key_size: int = 6,
    ) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(key_size))
