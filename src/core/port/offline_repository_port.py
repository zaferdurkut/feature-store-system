from typing import Protocol

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


class OfflineRepositoryPort(Protocol):
    def get_last_month_average_product_review_rating(
        self, product_id: str
    ) -> LastMonthAverageProductReviewRatingOutputModel:
        ...

    def get_last_month_category_revenue(
        self, category: str
    ) -> LastMonthCategoryRevenueOutputModel:
        ...

    def get_last_month_product_revenue(
        self, product_id: str
    ) -> LastMonthProductRevenueOutputModel:
        ...

    def get_last_month_sold_product_units(
        self, product_id: str
    ) -> LastMonthSoldProductUnitsOutputModel:
        ...
