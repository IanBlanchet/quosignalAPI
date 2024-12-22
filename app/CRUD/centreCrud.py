from sqlalchemy.orm import Session
from app import models, schemas

def get_centre(db : Session):
    return db.query(models.Centre).all()