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
from src.core.port.stream_repository_port import StreamRepositoryPort
from src.infra.config.open_tracing_config import tracer


class StreamService:
    def __init__(
        self,
        stream_repository_port: StreamRepositoryPort,
    ):
        self.stream_repository_port = stream_repository_port

    def get_product_review_rating_average(
        self, product_id: str
    ) -> ProductReviewRatingOutputModel:
        with tracer.start_active_span(
            "StreamService-get_product_review_rating_average",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "product_id",
                product_id,
            )
            return self.stream_repository_port.get_product_review_rating_average(
                product_id=product_id
            )

    def get_customer_last_purchase_amount(
        self, customer_id: str
    ) -> CustomerLastPurchaseAmountOutputModel:
        with tracer.start_active_span(
            "StreamService-get_customer_last_purchase_amount",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "customer_id",
                customer_id,
            )
            return self.stream_repository_port.get_customer_last_purchase_amount(
                customer_id=customer_id
            )

    def get_customer_last_product_review_rating(
        self, customer_id: str, product_id: str
    ) -> CustomerLastProductReviewRatingOutputModel:
        with tracer.start_active_span(
            "StreamService-get_customer_last_product_review_rating",
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
            return self.stream_repository_port.get_customer_last_product_review_rating(
                customer_id=customer_id, product_id=product_id
            )

    def get_total_revenue_order_by_category(
        self, category: str
    ) -> TotalRevenueByCategoryOutputModel:
        with tracer.start_active_span(
            "StreamService-get_total_revenue_order_by_category",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "category",
                category,
            )
            return self.stream_repository_port.get_total_revenue_order_by_category(
                category=category
            )
