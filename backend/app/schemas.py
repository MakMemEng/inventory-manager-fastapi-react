from pydantic import BaseModel
from typing import List, Optional

""" 各モデルに対応するPydanticモデルを定義
    これらは、入力データのバリデーションや、出力データのシリアライゼーションに使用される
"""
# Pydanticモデルを作成

class InventoryBase(BaseModel):
    material_id: int
    quantity: int
    stock_quantity: int
    unit_cost: int
    stock_price: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

    class Config:
        orm_mode = True

class MaterialBase(BaseModel):
    name: str
    category: str
    thickness: float
    copper_thickness: int
    size_x: int
    size_y: int
    maker: str
    material_type: str

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int
    inventories: List[Inventory] = []

    class Config:
        orm_mode = True
