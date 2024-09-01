from typing import Protocol

from src.core.model.stream.costumer_last_product_review_rating_output_model import \
    CustomerLastProductReviewRatingOutputModel
from src.core.model.stream.costumer_last_purchase_amount_output_model import CustomerLastPurchaseAmountOutputModel
from src.core.model.stream.product_view_rating_output_model import ProductReviewRatingOutputModel
from src.core.model.stream.total_revenue_by_category_output_model import TotalRevenueByCategoryOutputModel


class StreamRepositoryPort(Protocol):
    def get_product_review_rating_average(
        self, product_id: str
    ) -> ProductReviewRatingOutputModel:
        ...

    def get_customer_last_purchase_amount(
        self, customer_id: str
    ) -> CustomerLastPurchaseAmountOutputModel:
        ...

    def get_customer_last_product_review_rating(
        self, customer_id: str, product_id: str
    ) -> CustomerLastProductReviewRatingOutputModel:
        ...

    def get_total_revenue_order_by_category(
        self, category: str
    ) -> TotalRevenueByCategoryOutputModel:
        ...
