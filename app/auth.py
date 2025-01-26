from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException, APIRouter, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from pydantic import BaseModel, ValidationError
from typing import Annotated, Union
from app import models, schemas
from app.database import session_scope
from app.config import Config


def authenticate_usager(username: str, password:str, db: Session = Depends(session_scope)) -> models.Usager:
    """permet d'authentifier un usager

    Args:
        username (str): le nom d'usager, typiquement le courriel
        password (str): le mot de passe
        db (Session, optional): la base de donnée obtenu par dépendance(session_scope).

    Returns:
        _type_: Usager
    """
    usager = db.query(models.Usager).where(getattr(models.Usager, 'email') == username).first()
    #print(usager.hash_password(password))
    if not usager:        
        return False
    if not usager.verify_password(password):        
        return False
    return usager


class Token(BaseModel):
    access_token:str
    token_type : str

class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: list[str] = []

def get_user(username: str, db: Session = Depends(session_scope)):
    """permet d'obtenir un usager à partir d'un nom d'usager

    Args:
        username (str): le nom d'usager
        db (Session, optional): la connexion à la bd

    Returns:
        _type_: model pydantic BaseUsager
    """
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


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """création d'un token d'accès de type jwt

    Args:
        data (dict): les données à inclure au token typique {"sub": username,  "scopes": user_scopes}
        expires_delta (Union[timedelta, None], optional): la durée souhaitée avant l'expiration du token. Defaults to None.

    Returns:
        _type_: un token jwt
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm='HS256')
    return encoded_jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(
                                        tokenUrl="token",
                                        scopes={"benevole": "Read items and add call",}
                                        )


async def get_current_user(security_scopes: SecurityScopes,  token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(session_scope)):
    """permet de valider le token de l'usager courant

    Args:
        security_scopes (SecurityScopes): les scopes de base dans le schema OAuth2 déclaré
        token (Annotated[str, Depends): le token inclut dans l'appel sur l'URL
        db (Session, optional): la connexion à la base de données.

    Raises:
        credentials_exception: les messages obtenus sur validation des credentials
        HTTPException: les messages obtenus sur validation des credentials

    Returns:
        _type_: un usager sur le model pydantic
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":authenticate_value},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


@router.get("/usager/me")
async def read_users_me(current_user: Annotated[models.Usager, Depends(get_current_user)]):
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(session_scope)) -> Token:
    """la route pour se connecter sur l'api

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): les données provenant d'un formulaire (web, etc...)
        db (Session, optional): la connexion à la bd. Defaults to Depends(session_scope).

    Raises:
        HTTPException: les exception sur donnée du formulaire non valide

    Returns:
        Token: retourne un jeton sur un model pydantic
    """
    user= authenticate_usager(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token_expires = timedelta(minutes=720)
    user_scopes = []
    if user.niveau == 'modificateur':
        user_scopes.append('modificateur') 
    if user.niveau == 'admin':
        user_scopes += ['modificateur', 'admin']
    access_token = create_access_token(
        data={"sub": user.email,  "scopes": user_scopes}, 
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
    
