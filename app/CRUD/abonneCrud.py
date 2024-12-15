from sqlalchemy.orm import Session
from app import models, schemas

def get_abonne(db : Session):    
    return db.query(models.Abonne).all()

def create_abonne(db : Session, abonne :schemas.Abonne):
    new_abonne = models.Abonne(
        nom = abonne.nom,
        prenom = abonne.prenom,
        date_naissance = abonne.date_naissance,
        telephone = abonne.telephone
    )

    db.add(new_abonne)
    return new_abonne