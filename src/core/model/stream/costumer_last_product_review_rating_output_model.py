from pydantic import BaseModel


class CustomerLastProductReviewRatingOutputModel(BaseModel):
    rating: float
