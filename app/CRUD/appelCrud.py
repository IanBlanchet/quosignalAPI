from sqlalchemy.orm import Session
from app import models, schemas

def get_appel(db : Session):    
    return db.query(models.Appel).all()

def create_appel(db : Session, appel :schemas.BaseAppel):
    new_appel = models.Appel(
        date = appel.date,
        resultat = appel.resultat,
        alerte = appel.alerte,
        commentaire = appel.commentaire        
    )

    db.add(new_appel)
    return new_appel