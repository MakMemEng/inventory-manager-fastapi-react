from sqlalchemy.orm import Session
import models
import schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

def get_material(db: Session, material_id: int):
    return db.query(models.Material).filter(
        models.Material.id == material_id).first()


def get_materials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Material).offset(skip).limit(limit).all()


def create_material(db: Session, material: schemas.MaterialCreate):
    db_material = models.Material(
        name=material.name,
        category=material.category,
        thickness=material.thickness,
        copper_thickness=material.copper_thickness,
        size_x=material.size_x,
        size_y=material.size_y,
        maker=material.maker,
        material_type=material.material_type
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material
