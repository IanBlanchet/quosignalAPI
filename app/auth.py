from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException, APIRouter, Security, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from pydantic import BaseModel, ValidationError
from typing import Annotated, Union
from app import models, schemas
from app.database import session_scope
from app.config import Config
from app.util import fieldUniqueValidation
from app.email import EmailRequest


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
        return schemas.Usager(**user_dict)


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

router = APIRouter(prefix="/api/v1")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


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


@router.get("/usager/me", tags=["usager"])
async def read_users_me(current_user: Annotated[models.Usager, Depends(get_current_user)]):
    return current_user


@router.post("/token", tags=["auth"])
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
    user_scopes = {'attente':[], 'benevole':['benevole'], 'modificateur':['benevole', 'modificateur'], 'admin' : ['benevole', 'modificateur', 'admin']}
    access_token = create_access_token(
        data={"sub": user.email,  "scopes": user_scopes[user.niveau]}, 
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
    

@router.post("/usager/", tags=["usager"])
async def create_new_usager(user : schemas.NewUsager, db: Session = Depends(session_scope)) -> schemas.Usager:
    """permet de créer un nouvel usager

    Args:
        item (schemas.BaseUsager): les données de l'usager à créer
        db (Session, optional): la connexion à la bd. Defaults to Depends(session_scope).
        
    Returns:
        schemas.Usager: retourne un usager sur le model pydantic
    """
    user_dict = user.model_dump()
    fieldUniqueValidation(user_dict, ["email"], db, models.Usager)
    password = user_dict.pop('password')
    usager = models.Usager(**user_dict)
    usager.hash_password(password)    
    db.add(usager)
    db.commit()
    
    return usager

@router.post("/usager/{usager_id}/approval", tags=["usager"])
async def approve_new_usager(usager_id : int, niveau: str, db: Session = Depends(session_scope), current_user: Annotated[schemas.Usager, Security(get_current_user, scopes=['admin'])] = None) -> schemas.Usager:
    """permet d'approuver un usager par un admin

    Args:
        usager_id (int): l'id de l'usager à approuver
        niveau : le niveau d'autorisation de l'usager
        db (Session, optional): la connexion à la bd. Defaults to Depends(session_scope).

    Returns:
        schemas.Usager: retourne un usager sur le model pydantic
    """    
    usager = db.query(models.Usager).where(getattr(models.Usager, 'id') == usager_id).first()
    usager.niveau = schemas.niveauEnum[niveau]
    db.commit()
    return usager




@router.post("/reset_password_request", tags=["auth"])
async def reset_password_request(email: str, db: Session = Depends(session_scope)):
    """permet de demander la réinitialisation du mot de passe

    Args:
        email (str): le courriel de l'usager
        db (Session, optional): la connexion à la bd. Defaults to Depends(session_scope).

    Returns:
        dict: retourne un token utilisé pour réinitialiser le mot de passe
    """
    usager = db.query(models.Usager).where(getattr(models.Usager, 'email') == email).first()
    if not usager:
        raise HTTPException(status_code=400, detail="Cet usager n'existe pas")
    token = usager.get_reset_password_token()    

    return {"token": token}

@router.post("/reset_password", tags=["auth"])
async def reset_password(new_password: str = Form(...), token: str = None, db: Session = Depends(session_scope)):
    """permet de réinitialiser le mot de passe d'un usager

    Args:
        new_password (str): le noueau mot de passe
        token (str) : le token de réinitialisation obtenu par /reset_password_request
        db (Session, optional): la connexion à la bd. Defaults to Depends(session_scope).

    Returns:
        dict: retourne un message de succès
    """
    if not token:
        raise HTTPException(status_code=400, detail="aucun token n'est fourni")
    usager_id = models.Usager.verify_reset_password_token(token)
    if not usager_id:
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")
    usager = db.query(models.Usager).where(getattr(models.Usager, 'id') == usager_id).first()
    usager.hash_password(new_password)
    db.commit()
    return {"message": "Le mot de passe a été réinitialisé avec succès"}