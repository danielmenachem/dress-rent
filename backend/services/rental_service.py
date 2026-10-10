from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.rental import Rental
from backend.services.dress_service import get_dress
from backend.models.customer import Customer
from backend.services.customer_service import get_customer_by_id

# Check if a dress is available for rental between two dates, optionally excluding a specific rental ID from the check.
# Returns a tuple of three booleans: (available, pickup_sameday, return_sameday)
# - available: True if the dress is available for rental, False otherwise.
# - pickup_sameday: True if there is a rental that ends on the same day as the requested from_date, False otherwise.
# - return_sameday: True if there is a rental that starts on the same day as the requested to_date, False otherwise.
# Note - this implemtation does not allow one-day (or less) rentals
def is_available(
        session: Session,
        dress_id: int,
        from_date: date,
        to_date: date,
        exclude_rental_id: int | None = None
) -> tuple[bool, bool, bool]:
    if from_date >= to_date:
        raise ValueError("from_date cannot be later than to_date.")
    
    dress = get_dress(session, dress_id)

    if not dress.is_active:
        raise ValueError(f"Dress with ID {dress_id} is not active and cannot be rented.")
    
    # Check for overlapping rentals
    stmt = select(Rental).where(
        Rental.dress_id == dress_id,
        Rental.from_date < to_date,
        Rental.to_date > from_date,
        Rental.status != "cancelled"
    )

    if exclude_rental_id is not None:
        stmt = stmt.where(Rental.rental_id != exclude_rental_id)

    existing_rentals = session.scalars(stmt).first()
    available = existing_rentals is None
    
    pickup_stmt = select(Rental).where(
    Rental.dress_id == dress_id,
    Rental.to_date == from_date,
    Rental.status != "cancelled"
    )

    if exclude_rental_id is not None:
        pickup_stmt = pickup_stmt.where(
            Rental.rental_id != exclude_rental_id
        )

    pickup_sameday = session.scalars(pickup_stmt).first() is not None

    return_stmt = select(Rental).where(
        Rental.dress_id == dress_id,
        Rental.from_date == to_date,
        Rental.status != "cancelled"
    )

    if exclude_rental_id is not None:
        return_stmt = return_stmt.where(
            Rental.rental_id != exclude_rental_id
        )
    
    return_sameday = session.scalars(return_stmt).first() is not None

    return available, pickup_sameday, return_sameday



def create_rental(
        session: Session,
        dress_id: int,
        customer_id: int,
        from_date: date,
        to_date: date,
        discount: Decimal = Decimal("0.00"),
        extra_charges: Decimal = Decimal("0.00"),
        confirm_same_day: bool = False
) -> Rental:
    get_customer_by_id(session, customer_id)

    available, pickup_sameday, return_sameday = is_available(session, dress_id, from_date, to_date)

    if not available:
        raise ValueError(f"Dress with ID {dress_id} is not available for the selected dates.")
    
    if (pickup_sameday or return_sameday) and not confirm_same_day:
        raise ValueError("Same-day rental overlap requires confirmation.")
    
    dress = get_dress(session, dress_id)
    original_price = dress.price

    if extra_charges < 0:
        raise ValueError("Extra charges cannot be negative")

    if discount < 0 or discount > original_price + extra_charges:
        raise ValueError("Invalid discount amount")

    final_price = original_price + extra_charges - discount

    new_rental = Rental(
        dress_id=dress_id,
        customer_id=customer_id,
        from_date=from_date,
        to_date=to_date,
        original_price=original_price,
        discount=discount,
        extra_charges=extra_charges,
        final_price=final_price
    )

    session.add(new_rental)
    session.commit()
    session.refresh(new_rental)

    return new_rental

def get_rental(session: Session, rental_id: int) -> Rental:
    rental = session.get(Rental, rental_id)

    if rental is None:
        raise ValueError(f"Rental with ID {rental_id} not found.")
    
    return rental

def get_rentals(session: Session) -> list[Rental]:
    stmt = select(Rental)

    return list(session.scalars(stmt).all())

def update_rental(
        session: Session,
        rental_id: int,
        from_date: date | None = None,
        to_date: date | None = None,
        discount: Decimal | None = None,
        extra_charges: Decimal | None = None,
        confirm_same_day: bool = False
) -> Rental:
    rental = get_rental(session, rental_id)

    new_from_date = from_date if from_date is not None else rental.from_date
    new_to_date = to_date if to_date is not None else rental.to_date
    
    if new_from_date != rental.from_date or new_to_date != rental.to_date:
        available, pickup_sameday, return_sameday = is_available(
            session, 
            rental.dress_id,
            new_from_date,
            new_to_date,
            exclude_rental_id=rental_id
        )
        if not available:
            raise ValueError(f"Dress with ID {rental.dress_id} is not available for the updated dates.")
        
        if (pickup_sameday or return_sameday) and not confirm_same_day:
            raise ValueError("Same-day rental overlap requires confirmation.")
        
    new_extra_charges = extra_charges if extra_charges is not None else rental.extra_charges
    new_discount = discount if discount is not None else rental.discount

    if new_extra_charges < 0:
        raise ValueError("Extra charges cannot be negative")

    if new_discount < 0 or new_discount > rental.original_price + new_extra_charges:
        raise ValueError("Invalid discount amount")

    rental.from_date = new_from_date
    rental.to_date = new_to_date
    rental.extra_charges = new_extra_charges
    rental.discount = new_discount

    # Recalculate final price
    rental.final_price = rental.original_price + rental.extra_charges - rental.discount

    session.commit()
    session.refresh(rental)

    return rental

def cancel_rental(session: Session, rental_id:int) -> Rental:
    rental = get_rental(session, rental_id)

    if rental.status == "cancelled":
        raise ValueError(f"Rental with ID {rental_id} is already cancelled.")
    
    rental.status = "cancelled"

    session.commit()
    session.refresh(rental)

    return rental

def get_rentals_by_customer(session: Session, customer_id: int) -> list[Rental]:
    stmt = select(Rental).where(Rental.customer_id == customer_id)

    return list(session.scalars(stmt).all())

def get_rentals_by_dress(session: Session, dress_id: int) -> list[Rental]:
    stmt = select(Rental).where(Rental.dress_id == dress_id)

    return list(session.scalars(stmt).all())