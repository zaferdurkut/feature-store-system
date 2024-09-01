from fastapi import Depends, APIRouter

from starlette import status

from src.api.controller.auth.dto.login_output_dto import LoginOutputDto
from src.api.controller.auth.dto.login_user_input_dto import LoginUserInputDto
from src.api.controller.service_resolver import get_auth_service
from src.api.handler.error_response import ErrorResponse, generate_validation_error_response, generate_error_response
from src.core.model.auth.login_output_model import LoginOutputModel
from src.core.model.auth.login_user_input_model import LoginUserInputModel

router = APIRouter()



@router.post(
    "/login",
    response_model=LoginOutputDto,
    description="Login stream to the system.The system is dummy and does not have any stream. So, it will return dummy token. Use access_token to access endpoints.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": LoginOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "user_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
def login(
    login_user_input_dto: LoginUserInputDto,
    auth_service = Depends(get_auth_service),
):
    login_output_model: LoginOutputModel = auth_service.login(
        login_user_input_model=LoginUserInputModel(**login_user_input_dto.model_dump())
    )

    return LoginOutputDto(**login_output_model.model_dump())

