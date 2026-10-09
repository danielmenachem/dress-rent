from backend.database import engine
from backend.models.base import Base

from backend.models.dress import Dress
from backend.models.customer import Customer
from backend.models.rental import Rental

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")