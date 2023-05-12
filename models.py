from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

# 材料情報を管理するためのMaterialモデル
class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String)
    category = Column(String)
    thickness = Column(Float)
    copper_thickness = Column(Float)
    worksize = Column(String)
    manufacturer = Column(String)
    material_type = Column(String)
    price_per_unit = Column(Float)
    inventory = relationship("Inventory", back_populates="material")

# 在庫情報を管理するためのInventoryモデル
class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"))
    quantity = Column(Integer)
    material = relationship("Material", back_populates="inventory")

# ユーザー情報を管理するためのUserモデル
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
