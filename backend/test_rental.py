from decimal import Decimal

from backend.database import SessionLocal
from backend.models import dress, customer, rental
from backend.services.dress_service import add_dress
from backend.services.customer_service import add_customer
from datetime import date
from decimal import Decimal
from backend.services.rental_service import create_rental, update_rental, is_available, cancel_rental, get_rentals_by_customer, get_rentals_by_dress, get_rental

with SessionLocal() as session:
    rental = get_rental(session, rental_id=1)

    print("Customer:", rental.customer.first_name, rental.customer.last_name)
    print("Dress:", rental.dress.designer)
    print("Price:", rental.final_price)
    print("Status:", rental.status)