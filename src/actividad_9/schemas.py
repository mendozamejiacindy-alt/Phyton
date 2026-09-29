from datetime import datetime

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    product: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class OrderResponse(BaseModel):
    id: int
    product: str
    quantity: int
    price: float
    created_at: datetime

    model_config = {"from_attributes": True}
