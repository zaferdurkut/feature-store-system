from opentracing_instrumentation import get_current_span

from src.core.model.stream.costumer_last_product_review_rating_output_model import (
    CustomerLastProductReviewRatingOutputModel,
)
from src.core.model.stream.costumer_last_purchase_amount_output_model import (
    CustomerLastPurchaseAmountOutputModel,
)
from src.core.model.stream.product_view_rating_output_model import (
    ProductReviewRatingOutputModel,
)
from src.core.model.stream.total_revenue_by_category_output_model import (
    TotalRevenueByCategoryOutputModel,
)
from src.infra.adapter.repository.redis.repository_config import get_stream_redis_client
from src.infra.config.open_tracing_config import tracer
from src.infra.exception.not_found_exception import NotFoundException


class StreamCacheAdapter:
    def __init__(self):
        self.client = get_stream_redis_client()

    def get_product_review_rating_average(
        self, product_id: str
    ) -> ProductReviewRatingOutputModel:
        with tracer.start_active_span(
            "StreamCacheAdapter-get_product_review_rating_average",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "product_id",
                product_id,
            )
            key = f"avg_review:{product_id}"
            product_review_rating = self.client.get(key)
            if product_review_rating is None:
                raise NotFoundException(error_code=2003)
            return ProductReviewRatingOutputModel(
                avg_rating=float(product_review_rating.decode())
            )

    def get_customer_last_purchase_amount(
        self, customer_id: str
    ) -> CustomerLastPurchaseAmountOutputModel:
        with tracer.start_active_span(
            "StreamCacheAdapter-get_customer_last_order",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "customer_id",
                customer_id,
            )
            key = f"last_purchase_amount:{customer_id}"
            customer_last_order = self.client.get(key)
            if customer_last_order is None:
                raise NotFoundException(error_code=2004)

            return CustomerLastPurchaseAmountOutputModel(
                amount=float(customer_last_order.decode())
            )

    def get_customer_last_product_review_rating(
        self, customer_id: str, product_id: str
    ) -> CustomerLastProductReviewRatingOutputModel:
        with tracer.start_active_span(
            "StreamCacheAdapter-get_customer_last_product_review_rating",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "customer_id",
                customer_id,
            )
            scope.span.set_tag(
                "product_id",
                product_id,
            )
            key = f"last_review:{customer_id}_{product_id}"
            last_review = self.client.get(key)
            if last_review is None:
                raise NotFoundException(error_code=2005)
            return CustomerLastProductReviewRatingOutputModel(
                rating=float(last_review.decode())
            )

    def get_total_revenue_order_by_category(
        self, category: str
    ) -> TotalRevenueByCategoryOutputModel:
        with tracer.start_active_span(
            "StreamCacheAdapter-get_total_revenue_order_by_category",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "category",
                category,
            )
            key = f"revenue_category:{category}"
            total_revenue = self.client.get(key)
            if total_revenue is None:
                raise NotFoundException(error_code=2006)
            return TotalRevenueByCategoryOutputModel(
                revenue=float(total_revenue.decode())
            )
