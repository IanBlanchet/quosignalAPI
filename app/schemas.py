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
    centre_id : int

    model_config = {
        "from_attributes":True
        }     



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
    centre_id : int

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
    usager_id : int
    abonne_id : int

    model_config = {
        "from_attributes":True
        }     

class Appel(BaseAppel):    
    id : int

class Abonne(BaseAbonne):
    id: int
    date_insc : date
    actif : bool
    appels: List[Appel] = []

class Usager(BaseUsager):
    id : int
    appels: List[Appel] = []

class Centre(BaseModel):
    id : int
    nom : str
    adresse : str
    ville : str
    telephone : int
    usagers: List[Usager] = []
    abonnes: List[Abonne] = []

    model_config = {
        "from_attributes":True
        }     
