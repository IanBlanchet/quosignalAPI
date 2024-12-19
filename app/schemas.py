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

    class Config:
        from_attributes = True

class Abonne(BaseAbonne):
    id: int