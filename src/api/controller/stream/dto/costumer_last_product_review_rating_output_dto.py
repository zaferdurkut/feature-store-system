from pydantic import BaseModel, Field


class CustomerLastProductReviewRatingOutputDto(BaseModel):
    rating: float = Field(..., description="The rating of the product", examples=[4.5, 3.5])
