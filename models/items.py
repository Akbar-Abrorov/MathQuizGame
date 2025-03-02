from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import Base

class Item(Base):
    name: Mapped[str]
    amount: Mapped[int]
    price: Mapped[bool]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)