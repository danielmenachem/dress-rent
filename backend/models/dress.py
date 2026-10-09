from decimal import Decimal

from sqlalchemy import String, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class Dress(Base):
    __tablename__ = "dresses"
    
    dress_id: Mapped[int] = mapped_column(primary_key=True)

    designer: Mapped[str] = mapped_column(String(100))
    color: Mapped[str] = mapped_column(String(50))
    size: Mapped[str] = mapped_column(String(10))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image_path: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    dress_rentals: Mapped[list["Rental"]] = relationship(
        back_populates="dress"
    )