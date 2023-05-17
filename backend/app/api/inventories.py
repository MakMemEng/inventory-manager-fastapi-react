from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Inventory  # SQLAlchemyのモデル
from schemas import Inventory as InventorySchema  # Pydanticモデル
from schemas import InventoryBase

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/inventories", response_model=List[InventorySchema])
def read_inventories(skip: int = 0, limit: int = 100, db: Session = Depends(
    get_db)):
    inventories = db.query(Inventory).offset(skip).limit(limit).all()
    return inventories


@router.get("/inventories/{material_id}", response_model=InventorySchema)
def read_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Inventory).filter(Inventory.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return material


@router.post("/inventories", response_model=InventorySchema)
def create_material(material: InventoryBase, db: Session = Depends(get_db)):
    # 入力はInventoryBase
    db_material = Inventory(**material.dict())  # SQLAlchemyモデルのインスタンスを作成
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


@router.put("/inventories/{material_id}", response_model=InventorySchema)
def update_material(material_id: int, material: InventoryBase,
                    db: Session = Depends(get_db)):  # 入力はInventoryBase
    db_material = db.query(Inventory).filter(
        Inventory.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    for key, value in material.dict().items():
        setattr(db_material, key, value)  # フィールドを更新
    db.commit()
    db.refresh(db_material)
    return db_material


@router.delete("/inventories/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = db.query(Inventory).filter(
        Inventory.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    db.delete(db_material)
    db.commit()
    return {"detail": "Inventory deleted"}
