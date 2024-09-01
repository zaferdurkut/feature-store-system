from random import randint

from src.core.model.auth.login_output_model import LoginOutputModel
from src.core.model.auth.login_user_input_model import LoginUserInputModel
from src.core.model.auth.token_output_model import TokenOutputModel
from src.core.service.auth.auth_utils import AuthUtils
from src.infra.config.logging_config import get_logger

logger = get_logger()


class AuthService:
    def __init__(
        self,
    ):
        self.auth_utils = AuthUtils()

    def login(self, login_user_input_model: LoginUserInputModel) -> LoginOutputModel:
        # This is a dummy implementation. In a real-world scenario, you would
        token_output_model = TokenOutputModel(
            sub=str(randint(1, 1000)),
            roles=["stream"],
            email=login_user_input_model.email,
        )

        access_token = self.auth_utils.create_access_token(
            token_output_model=token_output_model
        )
        refresh_token = self.auth_utils.create_refresh_token(
            token_output_model=token_output_model
        )

        return LoginOutputModel(access_token=access_token, refresh_token=refresh_token)
