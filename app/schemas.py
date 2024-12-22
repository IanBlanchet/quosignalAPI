from typing import List, Union, Optional
from datetime import date, time
from pydantic import BaseModel


class BaseAbonne(BaseModel):
    nom : str
    prenom : str
    date_naissance : date
    telephone : int
    adresse : str
    ville : str
    heure : time     
    langue : Optional[str]  

    model_config = {
        "from_attributes":True
        }     

class Abonne(BaseAbonne):
    id: int
    date_insc : date
    actif : bool

class Centre(BaseModel):
    id : int
    nom : str
    adresse : str
    ville : str
    telephone : int
