from typing import List, Union, Optional
from datetime import date
from pydantic import BaseModel

class Abonne(BaseModel):
    id : int
    nom : str
    prenom : str
    date_naissance : date
    telephone : int

    class Config:
        from_attributes = True