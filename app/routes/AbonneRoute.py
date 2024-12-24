from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import app.CRUD.abonneCrud as abonneCrud

from app import schemas, models
from app.database import session_scope

router = APIRouter()

from app.routeFactory import RouteFactory

abonneRoute = RouteFactory('abonne', schemas.Abonne, schemas.BaseAbonne, models.Abonne)

allAbonneRouter = abonneRoute.create_route_get_all()

"""@router.get("/abonnes/", response_model=List[schemas.Abonne], tags=["abonnes"])
def read_abonne(db: Session = Depends(session_scope)):
    abonnes = abonneCrud.get_abonne(db)
    return abonnes"""

newAbonneRouter = abonneRoute.create_route_post_new(['heure', 'telephone'])
"""@router.post("/abonne/")
async def create_abonne(abonne: schemas.BaseAbonne, db: Session = Depends(session_scope)):
    
    return abonneCrud.create_abonne(db, abonne)"""



