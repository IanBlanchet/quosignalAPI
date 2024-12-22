from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import app.CRUD.centreCrud as centreCrud

from app import schemas
from app.database import session_scope

router = APIRouter()

@router.get("/centres/", response_model=List[schemas.Centre], tags=["centres"])
def read_centre(db: Session = Depends(session_scope)):
    centres = centreCrud.get_centre(db)
    return centres



