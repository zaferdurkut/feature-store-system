from datetime import datetime
from typing import List, Optional

import pytz
from fastapi import Request, HTTPException
from fastapi import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from src.core.model.auth.token_input_model import TokenInputModel
from src.core.service.auth.auth_utils import AUTH_ALGORITHM, JWT_SECRET_KEY
from src.infra.config.logging_config import get_logger
from src.infra.exception.not_found_exception import NotFoundException

logger = get_logger()


class CheckAuthService(HTTPBearer):
    def __init__(
        self,
        auto_error: bool = True,
        expected_user_roles: List[str] = [],
    ):
        super(CheckAuthService, self).__init__(auto_error=auto_error)

        self.expected_user_roles = expected_user_roles

    async def __call__(self, request: Request = None) -> TokenInputModel:

        try:
            credentials: HTTPAuthorizationCredentials = await super(
                CheckAuthService, self
            ).__call__(request)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated.",
            )

        user_token_model: TokenInputModel = self.authenticate_user(credentials)
        user_token_model.host = request.client.host

        self.authorize_user(
            token_input_model=user_token_model,
            expected_user_roles=self.expected_user_roles,
        )

        return user_token_model

    def authenticate_user(
        self, credentials: HTTPAuthorizationCredentials
    ) -> TokenInputModel:
        access_token = credentials.credentials
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme.",
            )
        token_input_model = self.verify_jwt_and_populate_token_input_model(access_token)
        # TODO: check Token from DB, Dummy implementation for now
        current_datetime = datetime.utcnow().replace(tzinfo=pytz.utc)
        if current_datetime > token_input_model.exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired. Please log in again or refresh your token.",
            )

        return token_input_model

    def authorize_user(
        self, token_input_model: TokenInputModel, expected_user_roles: List[str] = []
    ) -> bool:

        if len(expected_user_roles) == 0:
            # everyone is allowed on this endpoint
            has_access = True

        else:
            intersected_roles = set(token_input_model.roles) & set(expected_user_roles)

            if len(intersected_roles) > 0:
                has_access = True
            else:
                has_access = False

        if has_access is False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have the necessary permissions to access this resource.",
            )

        return has_access

    def verify_jwt_and_populate_token_input_model(
        self, jwt_token: str
    ) -> TokenInputModel:

        try:
            payload = self.decode_JWT(jwt_token=jwt_token)
            # TODO: check Token from DB, Dummy implementation for now
        except Exception as e:
            logger.error(f"JWT decode error: {e}")
            payload = None

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code.",
            )

        return TokenInputModel(**payload)

    def decode_JWT(self, jwt_token: str):
        try:
            payload = jwt.decode(jwt_token, JWT_SECRET_KEY, AUTH_ALGORITHM)
        except Exception as e:
            logger.error(f"JWT decode error: {e}")
            return None

        return payload
