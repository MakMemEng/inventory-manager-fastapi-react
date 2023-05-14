from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

""" 各クラスはテーブルのスキーマを定義し、そのフィールドはテーブルの列を表す。
    ForeignKeyは他のテーブルへのリンクを表す。
    relationshipはそのリンクを使用して他のテーブルとの関係を表す。
    
    モデル定義は、データベーススキーマを定義し、
    SQLAlchemy ORMを通じてデータベース操作を可能にする。
"""
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    inventory = relationship("Inventory", back_populates="user")

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    inventory = relationship("Inventory", back_populates="material")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    quantity = Column(Integer)

    user = relationship("User", back_populates="inventory")
    material = relationship("Material", back_populates="inventory")
