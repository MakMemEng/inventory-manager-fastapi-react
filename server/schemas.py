from pydantic import BaseModel
from typing import Optional

""" 各モデルに対応するPydanticモデルを定義
    これらは、入力データのバリデーションや、出力データのシリアライゼーションに使用される
"""
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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
