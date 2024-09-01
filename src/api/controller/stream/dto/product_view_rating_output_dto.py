from pydantic import BaseModel, Field


class ProductReviewRatingOutputDto(BaseModel):
    avg_rating: float = Field(..., description="The average rating of the product", examples=[4.5, 3.5])
