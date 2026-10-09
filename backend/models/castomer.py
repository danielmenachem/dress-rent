from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from base import Base

class Castomer(Base):
    __tablename__ = "castumers"

    castumer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(20))

