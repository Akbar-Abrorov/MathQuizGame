from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    points: int = 0
    double_points_active: bool = False

class UserCreate(UserBase):
    pass

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


