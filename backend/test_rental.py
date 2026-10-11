from decimal import Decimal

from backend.database import SessionLocal
from backend.models import dress, customer, rental
from backend.services.dress_service import add_dress
from backend.services.customer_service import add_customer
from datetime import date
from decimal import Decimal
from backend.services.rental_service import create_rental, update_rental, is_available, cancel_rental, get_rentals_by_customer, get_rentals_by_dress, get_rental

with SessionLocal() as session:
    rental = update_rental(
        session,
        rental_id=4,
        to_date=date(2026, 11, 19),
        confirm_same_day=True
    )

    print("Rental ID:", rental.rental_id)
    print("From:", rental.from_date)
    print("To:", rental.to_date)
    print("Status:", rental.status)