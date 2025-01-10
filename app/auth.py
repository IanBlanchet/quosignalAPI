from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from app import models, schemas
from app.database import session_scope


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")