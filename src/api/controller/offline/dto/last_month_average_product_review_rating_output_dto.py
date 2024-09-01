from pydantic import BaseModel, Field


class LastMonthAverageProductReviewRatingOutputDto(BaseModel):
    avg_rating: float = Field(..., description='Average rating of the product', examples=[4.5])
