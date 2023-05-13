from pydantic import BaseModel
from typing import Optional, List

class MaterialBase(BaseModel):
    material_name: Optional[str] = None
    category: Optional[str] = None
    thickness: Optional[float] = None
    copper_thickness: Optional[float] = None
    worksize: Optional[str] = None
    manufacturer: Optional[str] = None
    material_type: Optional[str] = None
    price_per_unit: Optional[float] = None


class MaterialCreate(MaterialBase):
    pass


class Material(MaterialBase):
    id: int
    inventories: List["Inventory"] = []

    class Config:
        orm_mode = True


class InventoryBase(BaseModel):
    material_id: Optional[int] = None
    quantity: Optional[int] = None


class InventoryCreate(InventoryBase):
    pass


class Inventory(InventoryBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
