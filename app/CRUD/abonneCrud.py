from sqlalchemy.orm import Session
from app import models, schemas

def get_abonne(db : Session):    
    return db.query(models.Abonne).all()

def create_abonne(db : Session, abonne :schemas.BaseAbonne):
    new_abonne = models.Abonne(
        nom = abonne.nom,
        prenom = abonne.prenom,
        date_naissance = abonne.date_naissance,
        telephone = abonne.telephone,        
        adresse = abonne.adresse,
        ville = abonne.ville,
        heure = abonne.heure
    )

    db.add(new_abonne)
    return new_abonne