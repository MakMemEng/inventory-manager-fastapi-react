from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal, engine

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


""" Userに対するCRUD操作のエンドポイント """
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_user(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate,
                db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user=user, user_id=user_id)


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)


""" Materialに対するCRUD操作のエンドポイント """
@app.post("/materials/", response_model=schemas.Material)
def create_material(material: schemas.MaterialCreate,
                    db: Session = Depends(get_db)):
    return crud.create_material(db=db, material=material)

# Materialの一覧を取得
@app.get("/materials/", response_model=List[schemas.Material])
def read_materials(skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db)):
    materials = crud.get_materials(db, skip=skip, limit=limit)
    return materials

# 特定のMaterialを取得
@app.get("/materials/{material_id}", response_model=schemas.Material)
def read_material(material_id: int, db: Session = Depends(get_db)):
    db_material = crud.get_material(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

# Materialを更新
@app.put("/materials/{material_id}", response_model=schemas.Material)
def update_material(material_id: int, material: schemas.MaterialCreate,
                    db: Session = Depends(get_db)):
    db_material = crud.get_material(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return crud.update_material(db=db, material=material,
                                material_id=material_id)

# Materialを削除
@app.delete("/materials/{material_id}", response_model=schemas.Material)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = crud.get_material(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return crud.delete_material(db=db, material_id=material_id)


""" Inventoryに対するCRUD操作のエンドポイント """
# 新規Inventoryを作成
@app.post("/inventory/", response_model=schemas.Inventory)
def create_inventory(inventory: schemas.InventoryCreate,
                     db: Session = Depends(get_db)):
    return crud.create_inventory(db=db, inventory=inventory)

# Inventoryの一覧を取得
@app.get("/inventory/", response_model=List[schemas.Inventory])
def read_inventory(skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db)):
    inventory = crud.get_inventory(db, skip=skip, limit=limit)
    return inventory

# 特定のInventoryを取得
@app.get("/inventory/{inventory_id}", response_model=schemas.Inventory)
def read_inventory(inventory_id: int, db: Session = Depends(get_db)):
    db_inventory = crud.get_inventory(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_inventory

# Inventoryを更新
@app.put("/inventory/{inventory_id}", response_model=schemas.Inventory)
def update_inventory(inventory_id: int, inventory: schemas.InventoryCreate,
                     db: Session = Depends(get_db)):
    db_inventory = crud.get_inventory(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return crud.update_inventory(db=db, inventory=inventory,
                                 inventory_id=inventory_id)

# Inventoryを削除
@app.delete("/inventory/{inventory_id}", response_model=schemas.Inventory)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    db_inventory = crud.get_inventory(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return crud.delete_inventory(db=db, inventory_id=inventory_id)
