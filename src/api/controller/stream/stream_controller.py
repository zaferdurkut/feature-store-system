from fastapi import APIRouter, Request, Depends, Query
from opentracing import Format
from opentracing.ext import tags
from starlette import status

from src.api.controller.service_resolver import (
    get_stream_service,
)
from src.api.controller.stream.dto.costumer_last_product_review_rating_output_dto import \
    CustomerLastProductReviewRatingOutputDto
from src.api.controller.stream.dto.costumer_last_purchase_amount_output_dto import CustomerLastPurchaseAmountOutputDto
from src.api.controller.stream.dto.product_view_rating_output_dto import (
    ProductReviewRatingOutputDto,
)
from src.api.controller.stream.dto.total_revenue_by_category_output_dto import TotalRevenueByCategoryOutputDto
from src.api.handler.error_response import (
    ErrorResponse,
    generate_validation_error_response,
    generate_error_response,
)
from src.core.model.auth.token_input_model import TokenInputModel
from src.core.model.stream.costumer_last_product_review_rating_output_model import \
    CustomerLastProductReviewRatingOutputModel
from src.core.model.stream.costumer_last_purchase_amount_output_model import CustomerLastPurchaseAmountOutputModel
from src.core.model.stream.product_view_rating_output_model import (
    ProductReviewRatingOutputModel,
)
from src.core.model.stream.total_revenue_by_category_output_model import TotalRevenueByCategoryOutputModel
from src.core.service.auth.authorization_roles import ROLE_ALL_ACTION
from src.core.service.auth.check_auth_service import CheckAuthService
from src.infra.config.open_tracing_config import tracer

router = APIRouter()


@router.get(
    "/review-rating-average",
    response_model=ProductReviewRatingOutputDto,
    description="The average rating of a last 5 product based on stream reviews.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": ProductReviewRatingOutputDto},
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
async def product_reviews_rating_average(
    request: Request,
    product_id: str = Query(..., description="Product ID", example="product_id"),
    stream_service=Depends(get_stream_service),
    user_token_model: TokenInputModel = Depends(
        CheckAuthService(expected_user_roles=ROLE_ALL_ACTION)
    ),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "StreamController-product_review_rating_average",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            product_review_rating_average_output_model: ProductReviewRatingOutputModel = (
                stream_service.get_product_review_rating_average(product_id=product_id)
            )
            return ProductReviewRatingOutputDto(
                **product_review_rating_average_output_model.model_dump()
            )
        finally:
            scope.close()

@router.get(
    "/customer-last-purchase-amount",
    response_model=CustomerLastPurchaseAmountOutputDto,
    description="The last purchase amount of a customer.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": CustomerLastPurchaseAmountOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "customer_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
async def customer_last_purchase_amount(
    request: Request,
    customer_id: str = Query(..., description="Customer ID", example="customer_id"),
    stream_service=Depends(get_stream_service),
    user_token_model: TokenInputModel = Depends(
        CheckAuthService(expected_user_roles=ROLE_ALL_ACTION)
    ),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "StreamController-customer_last_purchase_amount",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            customer_last_purchase_amount_output_model: CustomerLastPurchaseAmountOutputModel = (
                stream_service.get_customer_last_purchase_amount(customer_id=customer_id)
            )
            return CustomerLastPurchaseAmountOutputDto(
                **customer_last_purchase_amount_output_model.model_dump()
            )
        finally:
            scope.close()


@router.get(
    "/customer-last-product-review-rating",
    response_model=CustomerLastProductReviewRatingOutputDto,
    description="The last 5 products review rating of a customer.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": CustomerLastProductReviewRatingOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "customer_id", "product_id"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
async def customer_last_product_review_rating(
    request: Request,
    customer_id: str = Query(..., description="Customer ID", example="customer_id"),
    product_id: str = Query(..., description="Product ID", example="product_id"),
    stream_service=Depends(get_stream_service),
    user_token_model: TokenInputModel = Depends(
        CheckAuthService(expected_user_roles=ROLE_ALL_ACTION)
    ),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "StreamController-customer_last_product_review_rating",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            customer_last_product_review_rating_output_model: CustomerLastProductReviewRatingOutputModel = (
                stream_service.get_customer_last_product_review_rating(
                    customer_id=customer_id, product_id=product_id
                )
            )
            return CustomerLastProductReviewRatingOutputDto(
                **customer_last_product_review_rating_output_model.model_dump()
            )
        finally:
            scope.close()

# get_total_revenue_order_by_category
@router.get(
    "/total-revenue-by-category",
    response_model=TotalRevenueByCategoryOutputDto,
    description="The total revenue of last 3 order by category.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
    responses={
        status.HTTP_200_OK: {"model": TotalRevenueByCategoryOutputDto},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "content": generate_validation_error_response(
                invalid_field_location=["body", "category"]
            ),
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": generate_error_response(),
        },
    },
)
async def total_revenue_order_by_category(
    request: Request,
    category: str = Query(..., description="Category", example="category"),
    stream_service=Depends(get_stream_service),
    user_token_model: TokenInputModel = Depends(
        CheckAuthService(expected_user_roles=ROLE_ALL_ACTION)
    ),
):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
    }
    with tracer.start_active_span(
        "StreamController-total_revenue_order_by_category",
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        try:
            total_revenue_order_by_category_output_model: TotalRevenueByCategoryOutputModel = (
                stream_service.get_total_revenue_order_by_category(category=category)
            )
            return TotalRevenueByCategoryOutputDto(
                **total_revenue_order_by_category_output_model.model_dump()
            )
        finally:
            scope.close()
