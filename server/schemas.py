from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class MaterialBase(BaseModel):
    name: str
    description: Optional[str] = None

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int

    class Config:
        orm_mode = True

class InventoryBase(BaseModel):
    user_id: int
    material_id: int
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

    class Config:
        orm_mode = True
