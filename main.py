from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Material, Inventory
from schemas import MaterialCreate, Material

app = FastAPI()

# DBとの接続を開始
Base.metadata.create_all(bind=engine)

# DBとの接続を終了
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 材料をデータベースに登録
@app.post("/materials/", response_model=Material)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    db_material = Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

# データベースから材料を検索
@app.get("/materials/", response_model=List[Material])
def read_materials(skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db)):
    materials = db.query(Material).offset(skip).limit(limit).all()
    return materials

# データベースから材料を削除
@app.delete("/materials/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(db_material)
    db.commit()
    return {"message": "Material deleted"}
