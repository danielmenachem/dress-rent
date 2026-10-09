from decimal import Decimal
from datetime import date

from sqlalchemy import ForeignKey, Numeric, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base

class Rental(Base):
    __tablename__ = "rentals"

    rental_id: Mapped[int] = mapped_column(primary_key=True)

    dress_id: Mapped[int] = mapped_column(
        ForeignKey("dresses.dress_id")
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.customer_id")
    )
    
    dress: Mapped["Dress"] = relationship(
        back_populates="dress_rentals"
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="customer_rentals"
    )

    from_date: Mapped[date] = mapped_column(Date)
    to_date: Mapped[date] = mapped_column(Date)

    original_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    discount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00")
    )
    final_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    status: Mapped[str] = mapped_column(
        String(20),
        default="booked"
    )