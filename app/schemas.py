from typing import List, Union, Optional
from datetime import date, time
from pydantic import BaseModel

class Abonne(BaseModel):
    id : int
    nom : str
    prenom : str
    date_naissance : date
    telephone : int
    adresse : str
    ville : str
    heure : time

    class Config:
        from_attributes = True