from typing import List, Union, Optional
from datetime import date, time
from pydantic import BaseModel, EmailStr
from enum import Enum

class BaseAbonne(BaseModel):
    nom : str
    prenom : str
    date_naissance : date
    telephone : int
    adresse : str
    ville : str
    heure : time     
    langue : Optional[str]  
    centre : int

    model_config = {
        "from_attributes":True
        }     

class Abonne(BaseAbonne):
    id: int
    date_insc : date
    actif : bool


class niveauEnum(str, Enum):
    attente = 'attente'
    admin = 'admin'
    modificateur = 'modificateur'
    benevole = 'benevole'


class BaseUsager(BaseModel):    
    nom : str
    prenom : str
    email : EmailStr
    password_hash : Optional[str]
    niveau : niveauEnum
    centre : int

    model_config = {
        "from_attributes":True
        }     

class Usager(BaseUsager):
    id : int

class BaseAppel(BaseModel):    
    date : date
    resultat : str
    alerte : str
    commentaire: str
    usager : int
    abonne : int

    model_config = {
        "from_attributes":True
        }     

class Appel(BaseAppel):    
    id : int

class Centre(BaseModel):
    id : int
    nom : str
    adresse : str
    ville : str
    telephone : int

    model_config = {
        "from_attributes":True
        }     
