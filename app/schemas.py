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
        "from_attributes":True,        
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
    model_config = {
        "from_attributes":True
        } 


class Abonne(BaseAbonne):
    id: int
    date_insc : date
    actif : bool
    appels: List[Appel] = []
    

class Usager(BaseUsager):
    id : int
    appels: List[Appel] = []
    
class ContactUrgence(BaseContactUrgence):
    id : int 

class BaseAss_abonne_contactUrgence(BaseModel):
    """Association de base pour extraite la liste des contacts urgence
    """
    abonne_id : int
    contactUrgence_id : int
    lien : str
    
    model_config = {
        "from_attributes":True,              
        "arbitrary_types_allowed" : True
        } 
    
    def getLien(self):
        return self.lien

class ContactUrgence(ContactUrgence):
    """Contact d'urgence avec l'association a abonne
    """
    associations : List[BaseAss_abonne_contactUrgence] = []

class Abonne(Abonne):
    """Abonne complet lorsque retourné pour un get par item
    """
    contactUrgences : List[ContactUrgence] = []


class UpdateAss_abonne_contactUrgence(BaseAss_abonne_contactUrgence):
    """Ajout des abonne pour les requêtes sur contact urgence"""
    abonne : BaseAbonne

class ContactUrgence(ContactUrgence):
    """révision du contact d'urgence pour un appel complet sur l'item"""
    associations : List[UpdateAss_abonne_contactUrgence] = []

class Ass_abonne_contactUrgence(BaseAss_abonne_contactUrgence):
    """L'association complete"""
    abonne : Abonne
    contactUrgence : ContactUrgence
 
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
