from opentracing_instrumentation import get_current_span

from src.core.model.offline.last_month_average_product_review_rating_output_model import \
    LastMonthAverageProductReviewRatingOutputModel
from src.core.model.offline.last_month_category_revenue_output_model import LastMonthCategoryRevenueOutputModel
from src.core.model.offline.last_month_product_revenue_output_model import LastMonthProductRevenueOutputModel
from src.core.model.offline.last_month_sold_product_units_output_model import LastMonthSoldProductUnitsOutputModel
from src.infra.adapter.repository.redis.repository_config import get_offline_redis_client
from src.infra.config.open_tracing_config import tracer
from src.infra.exception.not_found_exception import NotFoundException


class OfflineCacheAdapter:
    def __init__(self):
        self.client = get_offline_redis_client()

    def get_last_month_average_product_review_rating(
        self, product_id: str
    ) -> LastMonthAverageProductReviewRatingOutputModel:
        with tracer.start_active_span(
            "OfflineCacheAdapter-get_last_month_average_product_review_rating",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "product_id",
                product_id,
            )
            key = f"avg_review_rating:{product_id}"
            product_review_rating = self.client.get(key)
            if product_review_rating is None:
                raise NotFoundException(error_code=2007)
            return LastMonthAverageProductReviewRatingOutputModel(
                avg_rating=float(product_review_rating.decode())
            )

    def get_last_month_category_revenue(
        self, category: str
    ) -> LastMonthCategoryRevenueOutputModel:
        with tracer.start_active_span(
            "OfflineCacheAdapter-get_last_month_category_revenue",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "category",
                category,
            )
            key = f"revenue_by_category:{category}"
            category_revenue = self.client.get(key)
            if category_revenue is None:
                raise NotFoundException(error_code=2008)
            return LastMonthCategoryRevenueOutputModel(
                revenue=float(category_revenue.decode())
            )

    def get_last_month_product_revenue(
        self, product_id: str
    ) -> LastMonthProductRevenueOutputModel:
        with tracer.start_active_span(
            "OfflineCacheAdapter-get_last_month_product_revenue",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "product_id",
                product_id,
            )
            key = f"revenue_by_product:{product_id}"
            product_revenue = self.client.get(key)
            if product_revenue is None:
                raise NotFoundException(error_code=2009)
            return LastMonthProductRevenueOutputModel(
                revenue=float(product_revenue.decode())
            )

    def get_last_month_sold_product_units(
        self, product_id: str
    ) -> LastMonthSoldProductUnitsOutputModel:
        with tracer.start_active_span(
            "OfflineCacheAdapter-get_last_month_sold_product_units",
            child_of=get_current_span(),
        ) as scope:
            scope.span.set_tag(
                "product_id",
                product_id,
            )
            key = f"units_sold:{product_id}"
            sold_units = self.client.get(key)
            if sold_units is None:
                raise NotFoundException(error_code=2010)
            return LastMonthSoldProductUnitsOutputModel(
                units=int(sold_units.decode())
            )
