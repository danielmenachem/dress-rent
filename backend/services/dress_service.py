from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.dress import Dress

def add_dress(
        session: Session,
        designer: str,
        color: str,
        size: str,
        price: Decimal,
        image_path: str
) -> Dress: 
    new_dress = Dress(
        designer=designer,
        color=color,
        size=size,
        price=price,
        image_path=image_path
    )

    session.add(new_dress)
    session.commit()
    session.refresh(new_dress)

    return new_dress

def update_dress(
        session: Session,
        dress_id: int,
        designer: str | None = None,
        color: str | None = None,
        size: str | None = None,
        price: Decimal | None = None,
        image_path: str | None = None
) -> Dress:
    dress = get_dress(session, dress_id)

    if designer is not None:
        dress.designer = designer

    if color is not None:
        dress.color = color

    if size is not None:
        dress.size = size

    if price is not None:
        dress.price = price

    if image_path is not None:
        dress.image_path = image_path

    session.commit()
    session.refresh(dress)

    return dress

def remove_dress(session: Session, dress_id: int) -> None:
    dress = get_dress(session, dress_id)

    if not dress.is_active:
        raise ValueError(f"Dress with id {dress_id} is already inactive")
    
    dress.is_active = False
    session.commit()


def get_dress(session: Session, dress_id: int) -> Dress:
    dress = session.get(Dress, dress_id)

    if dress is None:
        raise ValueError(f"Dress with id {dress_id} not found")
    
    return dress

def get_dresses(session: Session) -> list[Dress]:
    stmt = select(Dress).where(Dress.is_active.is_(True))

    return list(session.scalars(stmt).all())

def reactivate_dress(session: Session, dress_id: int) -> Dress:
    dress = get_dress(session, dress_id)

    if dress.is_active:
        raise ValueError(f"Dress with id {dress_id} is already active")
    
    dress.is_active = True
    session.commit()