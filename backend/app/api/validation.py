from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from api import crud
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_material_by_details(db: Session, material: schemas.MaterialCreate):
    return db.query(models.Material).filter(
        (models.Material.name == material.name) &
        (models.Material.category == material.category) &
        (models.Material.thickness == material.thickness) &
        (models.Material.copper_thickness == material.copper_thickness) &
        (models.Material.size_x == material.size_x) &
        (models.Material.size_y == material.size_y) &
        (models.Material.maker == material.maker) &
        (models.Material.material_type == material.material_type)
    ).first()
