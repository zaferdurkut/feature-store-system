from opentracing_instrumentation import get_current_span

from src.core.model.offline.last_month_average_product_review_rating_output_model import (
    LastMonthAverageProductReviewRatingOutputModel,
)
from src.core.model.offline.last_month_category_revenue_output_model import (
    LastMonthCategoryRevenueOutputModel,
)
from src.core.model.offline.last_month_product_revenue_output_model import (
    LastMonthProductRevenueOutputModel,
)
from src.core.model.offline.last_month_sold_product_units_output_model import (
    LastMonthSoldProductUnitsOutputModel,
)
from src.core.port.offline_repository_port import OfflineRepositoryPort
from src.infra.config.open_tracing_config import tracer


class OfflineService:
    def __init__(
        self,
        offline_repository_port: OfflineRepositoryPort,
    ):
        self.offline_repository_port = offline_repository_port

    def get_last_month_average_product_review_rating(
        self, product_id: str
    ) -> LastMonthAverageProductReviewRatingOutputModel:
        with tracer.start_active_span(
            "OfflineService-get_last_month_average_product_review_rating",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "product_id",
                product_id,
            )
            return self.offline_repository_port.get_last_month_average_product_review_rating(
                product_id=product_id
            )

    def get_last_month_category_revenue(
        self, category: str
    ) -> LastMonthCategoryRevenueOutputModel:
        with tracer.start_active_span(
            "OfflineService-get_last_month_category_revenue",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "category",
                category,
            )
            return self.offline_repository_port.get_last_month_category_revenue(
                category=category
            )

    def get_last_month_product_revenue(
        self, product_id: str
    ) -> LastMonthProductRevenueOutputModel:
        with tracer.start_active_span(
            "OfflineService-get_last_month_revenue_by_category",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "category",
                product_id,
            )
            return self.offline_repository_port.get_last_month_product_revenue(
                product_id=product_id
            )

    def get_last_month_sold_product_units(
        self, product_id: str
    ) -> LastMonthSoldProductUnitsOutputModel:
        with tracer.start_active_span(
            "OfflineService-get_last_month_sold_product_units",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "product_id",
                product_id,
            )
            return self.offline_repository_port.get_last_month_sold_product_units(
                product_id=product_id
            )
