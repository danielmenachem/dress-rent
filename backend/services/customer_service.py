from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.customer import Customer

def add_customer(
        session: Session,
        first_name: str,
        last_name: str,
        phone_number: str
    ) -> Customer:
    existing_customer = get_customer_by_phone(session, phone_number)

    if existing_customer:
        existing_customer_id = existing_customer.customer_id
        raise ValueError(f"Phone number {phone_number} is already in use by another customer {existing_customer_id}.")
    
    new_customer = Customer(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
    )

    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)

    return new_customer

def update_customer(
        session: Session,
        customer_id: int, 
        first_name: str | None = None,
        last_name: str | None = None,
        phone_number: str | None = None
    ) -> Customer:
    customer = get_customer_by_id(session, customer_id)

    if first_name is not None:
        customer.first_name = first_name

    if last_name is not None:
        customer.last_name = last_name
    
    if phone_number is not None:
        existing_customer = get_customer_by_phone(session, phone_number)

        if existing_customer and existing_customer.customer_id != customer_id:
            raise ValueError(f"Phone number {phone_number} is already in use by another customer.")
        
        customer.phone_number = phone_number
    
    session.commit()
    session.refresh(customer)

    return customer

def get_customer_by_id(session: Session, customer_id: int) -> Customer:
    customer = session.get(Customer, customer_id)

    if not customer:
        raise ValueError(f"Customer with ID {customer_id} not found.")
    
    return customer

def get_customer_by_phone(session: Session, phone_number: str) -> Customer | None:
    stmt = select(Customer).where(Customer.phone_number == phone_number)
    customer = session.scalars(stmt).first()

    return customer

def get_customers(session: Session) -> list[Customer]:
    stmt = select(Customer)
    return list(session.scalars(stmt).all())