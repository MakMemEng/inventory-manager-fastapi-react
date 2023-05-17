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
    name: Optional[str] = None
    category: Optional[str] = None
    thickness: Optional[float] = None
    copper_thickness: Optional[int] = None
    size_x: Optional[int] = None
    size_y: Optional[int] = None
    maker: Optional[str] = None
    material_type: Optional[str] = None

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int
    inventories: List[Inventory] = []

    class Config:
        orm_mode = True
