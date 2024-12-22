from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import app.CRUD.appelCrud as appelCrud

from app import schemas
from app.database import session_scope

router = APIRouter()

@router.get("/appels/", response_model=List[schemas.Appel], tags=["appels"])
def read_appel(db: Session = Depends(session_scope)):
    appels = appelCrud.get_appel(db)
    return appels


@router.post("/appel/")
async def create_appel(appel: schemas.BaseAppel, db: Session = Depends(session_scope)):
    
    return appelCrud.create_appel(db, appel)