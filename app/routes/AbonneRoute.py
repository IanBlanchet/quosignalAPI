from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import app.CRUD.abonneCrud as abonneCrud

from app import schemas
from app.database import session_scope

router = APIRouter()

@router.get("/abonnes/", response_model=List[schemas.Abonne], tags=["abonnes"])
def read_abonne(db: Session = Depends(session_scope)):
    abonnes = abonneCrud.get_abonne(db)
    return abonnes
