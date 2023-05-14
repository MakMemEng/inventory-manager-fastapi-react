from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


""" 各関数は、SQLAlchemyのSessionオブジェクトと、操作を行う対象のスキーマを引数にとる。
    また、**.dict()を使用して、スキーマからモデルを作成する。
    そして、作成したモデルをデータベースに追加し、コミットを行う。
    最後に、データベースから新しいエントリを取得して返す。
"""
""" Userに関する操作 """
def get_user(db: Session, user_id: int):
    return get_object_or_none(db, models.User, user_id)


def get_all_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    db_user = get_object_or_none(db, models.User, user_id)
    return update_object(db, db_user, user)


def delete_user(db: Session, user_id: int):
    db_user = get_object_or_none(db, models.User, user_id)
    return delete_object(db, db_user)


""" Materialに関する操作 """
def get_material(db: Session, material_id: int):
    return get_object_or_none(db, models.Material, material_id)

# 全ての材料を取得
def get_all_materials(db: Session):
    return db.query(models.Material).all()


def create_material(db: Session, material: schemas.MaterialCreate):
    db_material = models.Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def update_material(db: Session, material: schemas.MaterialCreate, material_id: int):
    db_material = get_object_or_none(db, models.Material, material_id)
    return update_object(db, db_material, material)


def delete_material(db: Session, material_id: int):
    db_material = get_object_or_none(db, models.Material, material_id)
    return delete_object(db, db_material)


""" Inventoryに関する操作 """
def get_inventory(db: Session, inventory_id: int):
    return get_object_or_none(db, models.Inventory, inventory_id)

# 全ての材料を取得
def get_all_inventory(db: Session):
    return db.query(models.Inventory).all()


def create_inventory(db: Session, inventory: schemas.InventoryCreate):
    db_inventory = models.Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


# Inventoryを更新する関数
def update_inventory(db: Session, inventory: schemas.InventoryCreate, inventory_id: int):
    db_inventory = get_object_or_none(db, models.Inventory, inventory_id)
    return update_object(db, db_inventory, inventory)

# Inventoryを削除する関数
def delete_inventory(db: Session, inventory_id: int):
    db_inventory = get_object_or_none(db, models.Inventory, inventory_id)
    return delete_object(db, db_inventory)


# ヘルパー関数
def get_object_or_none(db: Session, model: models, object_id: int):
    db_object = db.query(model).filter(model.id == object_id).first()
    return db_object


def delete_object(db: Session, db_object):
    if db_object is None:
        return None
    db.delete(db_object)
    db.commit()
    return db_object


def update_object(db: Session, db_object, schema):
    if db_object is None:
        return None
    for var, value in vars(schema).items():
        setattr(db_object, var, value) if value else None
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


""" JWTに関する操作 """
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "SECRET_KEY", algorithm="HS256")
    return encoded_jwt
