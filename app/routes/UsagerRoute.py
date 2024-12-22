from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import app.CRUD.usagerCrud as usagerCrud

from app import schemas
from app.database import session_scope

router = APIRouter()

@router.get("/usagers/", response_model=List[schemas.Usager], tags=["usagers"])
def read_usager(db: Session = Depends(session_scope)):
    usagers = usagerCrud.get_usager(db)
    return usagers


@router.post("/usager/")
async def create_usager(usager: schemas.BaseUsager, db: Session = Depends(session_scope)):
    new_usager = usagerCrud.create_usager(db, usager)
    if not new_usager:
        raise HTTPException(status_code=400, detail="Email existe déjà")
    return new_usager