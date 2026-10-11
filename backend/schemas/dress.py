from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class DressResponse(BaseModel):
    dress_id: int
    designer: str
    color: str
    size: str
    price: Decimal
    image_path: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class DressCreate(BaseModel):
    designer: str
    color: str
    size: str
    price: Decimal
    image_path: str | None = None

class DressUpdate(BaseModel):
    designer: str | None = None
    color: str | None = None
    size: str | None = None
    price: Decimal | None = None
    image_path: str | None = None