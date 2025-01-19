from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated, Union
from app import models, schemas
from app.database import session_scope
from app.config import Config


def authenticate_usager(username: str, password:str, db: Session = Depends(session_scope)):
    usager = db.query(models.Usager).where(getattr(models.Usager, 'email') == username).first()
    print(usager.hash_password(password))
    if not usager:
        print('pas usager')
        return False
    if not usager.verify_password(password):
        print('mauvais pass')
        return False
    return usager

'''fake_users_db = {
    "johndoe": {
        "nom": "johndoe",
        "prenom": "John Doe",
        "email": "johndoe@example.com",
        "password_hash": "fakehashedsecret",
        "niveau": "benevole",
        "centre_id":1
    },
    "alice": {
        "nom": "alice",
        "prenom": "Alice Wonderson",
        "email": "alice@example.com",
        "password_hash": "fakehashedsecret2",
        "niveau": "benevole",
        "centre_id":1
    },
}'''

class Token(BaseModel):
    access_token:str
    token_type : str

class TokenData(BaseModel):
    username: Union[str, None] = None

def get_user(username: str, db: Session = Depends(session_scope)):
    usager = db.query(models.Usager).where(getattr(models.Usager, 'email') == username).first()
    if usager:
        user_dict = { 
            "id": usager.id, 
            "nom": usager.nom, 
            "prenom": usager.prenom, 
            "email": usager.email, 
            "password_hash": usager.password_hash, 
            "niveau": usager.niveau, 
            "centre_id": usager.centre_id }       
        return schemas.BaseUsager(**user_dict)

'''def fake_hash_password(password: str):
    return "fakehashed" + password'''

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm='HS256')
    return encoded_jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

'''def fake_decode_token(token):
    return models.Usager(
        nom=token + "fakedecoded", email="john@example.com", prenom="John Doe"
    )'''


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(session_scope)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


@router.get("/usager/me")
async def read_users_me(current_user: Annotated[models.Usager, Depends(get_current_user)]):
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(session_scope)) -> Token:
    user= authenticate_usager(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token_expires = timedelta(minutes=720)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
    
