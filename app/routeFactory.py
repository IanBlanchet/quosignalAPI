from sqlalchemy.orm import Session
from app import models, schemas
from typing import List

from fastapi import Depends, HTTPException, APIRouter


from app.database import session_scope


router = APIRouter()

class RouteFactory:
    def __init__(self, routename, schema, baseSchema, model):
        self.routename = routename
        self.schema = schema
        self.baseSchema = baseSchema
        self.model = model
        self.router = router

    def create_route_get_all(self): 
        @self.router.get(f"/{self.routename}/", response_model=List[self.schema], tags=[self.routename]) 
        def read_all(db: Session = Depends(session_scope)):
            items = db.query(self.model).all() 
            return items
        return self.router

    def create_route_post_new(self, fieldUniqueValidation : List[str]):
        @self.router.post(f"/{self.routename}/" ) 
        def create_new(item : self.baseSchema, db: Session = Depends(session_scope)):
            for field in fieldUniqueValidation:
                existItem = db.query(self.model).where(self.model[field] == item[field]).first()
                if existItem:
                    raise HTTPException(status_code=400, detail=f"{field} existe déjà")

            item_dict = item.dict()
            new_item = self.model(**item_dict)
            db.add(new_item)
            return new_item
        return self.router








