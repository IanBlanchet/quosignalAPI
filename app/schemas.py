from typing import List, Union, Optional, Dict, Any
from datetime import date, time
from pydantic import BaseModel, EmailStr
from enum import Enum

class BaseAbonne(BaseModel):
    nom : str
    prenom : str
    date_naissance : date
    telephone : int
    telephone2 : Union[int, None] = None
    adresse : str
    ville : str
    heure : time     
    langue : Optional[str] 
    noCle : Union[int, None] = None 
    infoSupp : Union[Dict, None] = {} #Any = {}
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

class BaseContactUrgence(BaseModel):    
    nomComplet : str
    telephone : int
    telephone2 : Union[int, None] = None
    cleDispo : bool = False
    lien : str
    model_config = {
        "from_attributes":True
        } 


class Abonne(BaseAbonne):
    id: int
    date_insc : date
    actif : bool
    appels: List[Appel] = []
    contactUrgences : List[BaseContactUrgence] = []

class Usager(BaseUsager):
    id : int
    appels: List[Appel] = []
    
class ContactUrgence(BaseContactUrgence):
    id : int 
    abonnes : List[Abonne] = []

class Ass_abonne_contactUrgence(BaseModel):
    abonne : List[Abonne] = []
    contactUrgence : List[BaseContactUrgence] = []
    
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
