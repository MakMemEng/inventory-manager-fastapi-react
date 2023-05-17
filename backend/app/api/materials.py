from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from api import crud
import models  # SQLAlchemyのモデル
import schemas  # Pydanticモデル

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def insert_test_data():
    # セッションを作成
    session = SessionLocal()

    try:
        # テストデータを作成
        test_material = models.Material(
            name="AC-7004",
            category="片面アルミ",
            thickness=1.0,
            copper_thickness=35,
            size_x=510,
            size_y=255,
            maker='R工業',
            material_type='アルミベース基板'
        )

        # テストデータをデータベースに追加
        session.add(test_material)

        # 変更をコミット（データベースに保存）
        session.commit()

    except Exception as e:
        # エラーが発生した場合、ロールバック（変更の取り消し）を行います
        session.rollback()
        print(f"An error occurred: {e}")

    finally:
        # 最後に、エラーが発生しようがしまいが、セッションを閉じます
        session.close()


@router.post("/materials", response_model=schemas.Material)
async def create_material(material: schemas.MaterialCreate,
                          db: Session = Depends(get_db)):
    # 入力はMaterialBase
    db_material = crud.create_material(db=db, **material.dict())  #
    if db_material:
        raise HTTPException(status_code=400, detail="既に登録済みの材料です")
    # SQLAlchemyモデルのインスタンスを作成
    return db_material


@router.get("/materials", response_model=List[schemas.Material])
async def read_materials(skip: int = 0, limit: int = 100,
                         db: Session = Depends(get_db)):
    materials = crud.get_materials(db, skip=skip, limit=limit)
    return materials


@router.get("/materials/{material_id}", response_model=schemas.Material)
def read_material(material_id: int, db: Session = Depends(get_db)):
    material = crud.get_material(db, material_id=material_id)
    if material is None:
        raise HTTPException(status_code=404, detail="指定の材料が見つかりません")
    return material


@router.put("/materials/{material_id}", response_model=schemas.Material)
def update_material(material_id: int, material: schemas.MaterialBase,
                    db: Session = Depends(get_db)):  # 入力はMaterialBase
    db_material = crud.get_material(db=db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    for key, value in material.dict().items():
        setattr(db_material, key, value)  # フィールドを更新
    db.commit()
    db.refresh(db_material)
    return db_material


@router.delete("/materials/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = crud.get_material(db=db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(db_material)
    db.commit()
    return {"detail": "Material deleted"}
