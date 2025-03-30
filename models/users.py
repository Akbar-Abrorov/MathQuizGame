from sqlalchemy.orm import Mapped, relationship


from .base import Base
from typing import List
from models.items import Item
from models.questions import Question

class User(Base):
    name: Mapped[str]
    points: Mapped[int]
    double_points_active: Mapped[bool]
    # questions: Mapped[List["Question"]]= relationship(back_populates="user", cascade="all, delete-orphan")
    # items: Mapped[List["Item"]]= relationship(back_populates="user", cascade="all, delete-orphan")
