from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import Base

class Question(Base):
    question: Mapped[str]
    answer: Mapped[int]
    checked: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)



