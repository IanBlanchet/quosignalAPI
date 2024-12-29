from sqlalchemy.orm import Session
from app import models, schemas

def get_usager(db : Session):    
    return db.query(models.Usager).all()

def create_usager(db : Session, usager :schemas.BaseUsager):
    existUsager = db.query(models.Usager).where(models.Usager.email == usager.email).first()    
    if existUsager:
        return None
    
    new_usager = models.Usager(
        nom = usager.nom,
        prenom = usager.prenom,
        email = usager.email,
        password_hash = usager.password_hash,
        niveau = usager.niveau
    )

    db.add(new_usager)
    return new_usager



