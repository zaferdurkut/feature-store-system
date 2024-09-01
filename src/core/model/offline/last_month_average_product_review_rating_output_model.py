from pydantic import BaseModel


class LastMonthAverageProductReviewRatingOutputModel(BaseModel):
    avg_rating: float
