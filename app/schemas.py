from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DeliveryCreate(BaseModel):
    recipient: str = Field(min_length=1, max_length=120)
    address: str = Field(min_length=1, max_length=255)
    item: str = Field(min_length=1, max_length=255)
    status: str = Field(default="pending", max_length=32)


class DeliveryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recipient: str
    address: str
    item: str
    status: str
    created_at: datetime
