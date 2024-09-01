from fastapi import APIRouter, Request, Depends, Query
from opentracing import Format
from opentracing.ext import tags
from starlette import status

from src.api.controller.offline.dto.last_month_average_product_review_rating_output_dto import (
    LastMonthAverageProductReviewRatingOutputDto,
)
from src.api.controller.offline.dto.last_month_category_revenue_output_dto import (
    LastMonthCategoryRevenueOutputDto,
)
from src.api.controller.offline.dto.last_month_product_revenue_output_dto import LastMonthProductRevenueOutputDto
from src.api.controller.offline.dto.last_month_sold_product_units_output_dto import LastMonthSoldProductUnitsOutputDto
from src.api.controller.service_resolver import (
    get_offline_service,
)
from src.api.handler.error_response import (
    ErrorResponse,
    generate_validation_error_response,
    generate_error_response,
)
from src.core.model.auth.token_input_model import TokenInputModel
from src.core.model.offline.last_month_average_product_review_rating_output_model import (
    LastMonthAverageProductReviewRatingOutputModel,
)
from src.core.model.offline.last_month_category_revenue_output_model import (
    LastMonthCategoryRevenueOutputModel,
)
from src.core.model.offline.last_month_product_revenue_output_model import LastMonthProductRevenueOutputModel
from src.core.model.offline.last_month_sold_product_units_output_model import LastMonthSoldProductUnitsOutputModel
from src.core.service.auth.authorization_roles import ROLE_ALL_ACTION
from src.core.service.auth.check_auth_service import CheckAuthService
from src.infra.config.open_tracing_config import tracer

router = APIRouter()


@router.get(
    "/average-product-review-rating",
    response_model=LastMonthAverageProductReviewRatingOutputDto,
    description="Get the average rating of a product in the last month.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": LastMonthAverageProductReviewRatingOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "product_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
async def last_month_average_product_review_rating(
    request: Request,
    product_id: str = Query(..., description="Product ID", example="product_id"),
    offline_service=Depends(get_offline_service),
    user_token_model: TokenInputModel = Depends(
        CheckAuthService(expected_user_roles=ROLE_ALL_ACTION)
    ),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "OfflineController-get_last_month_average_product_review_rating",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            last_month_average_product_review_rating_output_model: LastMonthAverageProductReviewRatingOutputModel = offline_service.get_last_month_average_product_review_rating(
                product_id=product_id
            )
            return LastMonthAverageProductReviewRatingOutputDto(
                **last_month_average_product_review_rating_output_model.model_dump()
            )
        finally:
            scope.close()


@router.get(
    "/category-revenue",
    response_model=LastMonthCategoryRevenueOutputDto,
    description="Get the revenue of a category in the last month.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": LastMonthCategoryRevenueOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "product_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
async def last_month_category_revenue(
    request: Request,
    category: str = Query(..., description="Category", example="category"),
    offline_service=Depends(get_offline_service),
    user_token_model: TokenInputModel = Depends(
        CheckAuthService(expected_user_roles=ROLE_ALL_ACTION)
    ),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "OfflineController-get_last_month_category_revenue",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            last_month_category_revenue_output_model: LastMonthCategoryRevenueOutputModel = offline_service.get_last_month_category_revenue(
                category=category
            )
            return LastMonthCategoryRevenueOutputDto(
                **last_month_category_revenue_output_model.model_dump()
            )
        finally:
            scope.close()



@router.get(
    "/product-revenue",
    response_model=LastMonthProductRevenueOutputDto,
    description="Get the revenue of a product in the last month.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": LastMonthProductRevenueOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "product_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
async def last_month_product_revenue(
    request: Request,
    product_id: str = Query(..., description="Product ID", example="product_id"),
    offline_service=Depends(get_offline_service),
    user_token_model: TokenInputModel = Depends(
        CheckAuthService(expected_user_roles=ROLE_ALL_ACTION)
    ),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "OfflineController-get_last_month_product_revenue",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            last_month_product_revenue_output_model: LastMonthProductRevenueOutputModel = offline_service.get_last_month_product_revenue(
                product_id=product_id
            )
            return LastMonthProductRevenueOutputDto(
                **last_month_product_revenue_output_model.model_dump()
            )
        finally:
            scope.close()



@router.get(
    "/sold-product-units",
    response_model=LastMonthSoldProductUnitsOutputDto,
    description="Get the sold units of a product in the last month.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": LastMonthSoldProductUnitsOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "product_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
async def last_month_sold_product_units(
    request: Request,
    product_id: str = Query(..., description="Product ID", example="product_id"),
    offline_service=Depends(get_offline_service),
    user_token_model: TokenInputModel = Depends(
        CheckAuthService(expected_user_roles=ROLE_ALL_ACTION)
    ),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "OfflineController-get_last_month_sold_product_units",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            last_month_sold_product_units_output_model: LastMonthSoldProductUnitsOutputModel = offline_service.get_last_month_sold_product_units(
                product_id=product_id
            )
            return LastMonthSoldProductUnitsOutputDto(
                **last_month_sold_product_units_output_model.model_dump()
            )
        finally:
            scope.close()

