from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.rental import Rental
from backend.services.dress_service import get_dress
from backend.models.customer import Customer

# is it possible to return and take the dress on the same day? if yes, then the following function should be 
# modified to allow that
def is_available(
        session: Session,
        dress_id: int,
        from_date: date,
        to_date: date
) -> bool:
    if from_date > to_date:
        raise ValueError("from_date cannot be later than to_date.")
    
    dress = get_dress(session, dress_id)

    if not dress.is_active:
        raise ValueError(f"Dress with ID {dress_id} is not active and cannot be rented.")
    
    stmt = select(Rental).where(
        Rental.dress_id == dress_id,
        Rental.from_date <= to_date,
        Rental.to_date >= from_date,
        Rental.status != "cancelled"
    )

    existing_rentals = session.scalars(stmt).first()

    return existing_rentals is None

def create_rental(
        session: Session,
        dress_id: int,
        customer_id: int,
        from_date: date,
        to_date: date,
        original_price: Decimal,
        discount: Decimal = Decimal("0.00")
) -> Rental:
    customer = session.get(Customer, customer_id)

    if not is_available(session, dress_id, from_date, to_date):
        raise ValueError(f"Dress with ID {dress_id} is not available for the selected dates.")
    
    dress = get_dress(session, dress_id)
    original_price = dress.price

    if discount < Decimal("0.00") or discount > original_price:
        raise ValueError(f"Discount must be between 0 and the original price of {original_price}.")

    final_price = original_price - discount

    new_rental = Rental(
        dress_id=dress_id,
        customer_id=customer_id,
        from_date=from_date,
        to_date=to_date,
        original_price=original_price,
        discount=discount,
        extra_charges=Decimal("0.00"),
        final_price=final_price
    )

    session.add(new_rental)
    session.commit()
    session.refresh(new_rental)

    return new_rental
