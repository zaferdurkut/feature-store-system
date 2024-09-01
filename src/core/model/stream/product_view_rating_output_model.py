from pydantic import BaseModel


class ProductReviewRatingOutputModel(BaseModel):
    avg_rating: float
