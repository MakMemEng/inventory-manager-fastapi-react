from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    thickness = Column(Float)
    copper_thickness = Column(Integer)
    size_x = Column(Integer)
    size_y = Column(Integer)
    maker = Column(String, index=True)
    material_type = Column(String, index=True)

    inventory = relationship("Inventory", back_populates="material")

class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    stock_quantity = Column(Integer)
    unit_cost = Column(Integer)
    stock_price = Column(Integer)  # stock_quantity * unit_cost

    # user = relationship("User", back_populates="inventory")
    material = relationship("Material", back_populates="inventory")
