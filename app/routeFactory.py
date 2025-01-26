from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app import models, schemas
from typing import List, Annotated

from fastapi import Depends, HTTPException, APIRouter, Security
from app.auth import oauth2_scheme, get_current_user


from app.database import session_scope


router = APIRouter(dependencies=[Depends(get_current_user)])

class RouteFactory:
    """
        permet de créer un objet pour générer des routes
        Args : 
            routename (str) : le nom de la route (url)
            schema (schemas) : le schema pydantic complet
            baseSchema (schema) : le schema pydantic de base
            model (models) : le model de l'orm sql_alchemy
            relations (List) : la liste des relations qui doivent être jointent dans l'appel sur l'orm        
    """
    def __init__(self, routename : str, schema : schemas, baseSchema : schemas, model : models, relations : list = []) -> object:
        self.routename = routename
        self.schema = schema
        self.baseSchema = baseSchema
        self.model = model
        self.relations = relations
        self.router = router

    def create_route_get_all(self) -> APIRouter: 
        "retourne un router pour obtenir toutes les données"
        @self.router.get(f"/{self.routename}/", response_model=List[self.baseSchema], tags=[self.routename]) 
        def read_all(db: Session = Depends(session_scope) ):
            items = db.query(self.model).all() 
            return items
        return self.router
    
    def create_route_get_item(self) -> APIRouter:
        """une route pour récupérer un item

        Raises:
            HTTPException: lorsque l'item n'existe pas

        Returns:
            APIRouter: une route pour obtenir un item spécifique basé sur l'url
        """
        @self.router.get(f"/{self.routename}/"+"{item_id}", response_model=self.schema, tags=[self.routename])
        def read_item(item_id: int, db: Session = Depends(session_scope)):
            query = db.query(self.model)#.where(getattr(self.model, 'id') == item_id).first()
            for relation in self.relations: 
                query = query.options(joinedload(getattr(self.model, relation)))
            item = query.where(getattr(self.model, 'id') == item_id).first()
            if not item:
                raise HTTPException(status_code=400, detail=f"Cet {self.routename} n'existe pas ")

            return item
        return self.router

    def create_route_post_new(self, fieldUniqueValidation : List[str], niveau : List[str] = []) -> APIRouter:
        """
        permet de creer une route pour creer une nouvelle entrée

        Args: 
            fieldUniqueValidation (List): les noms du champs qui doivent être unique.  
                                        Si le champs est une liste, on veut valider une combinaison.
            niveau (str) : permet de controler l'autorisation requise pour utiliser cette route
        """
        @self.router.post(f"/{self.routename}/", tags=[self.routename] ) 
        def create_new(item : self.baseSchema, db: Session = Depends(session_scope), current_user: Annotated[self.schema, Security(get_current_user, scopes=niveau)] = None):
            item_dict = item.dict()
            for field in fieldUniqueValidation:
                if type(field) == list:
                    existItem = db.query(self.model).where(and_(getattr(self.model, field[0]) == item_dict[field[0]] , getattr(self.model, field[1]) == item_dict[field[1]])).first()
                    if existItem:
                        raise HTTPException(status_code=400, detail=f"La combinaison {field[0]} et {field[1]} existe déjà")
                else:
                    existItem = db.query(self.model).where(getattr(self.model, field) == item_dict[field]).first()
                    if existItem:
                        raise HTTPException(status_code=400, detail=f"{field} existe déjà")

            new_item = self.model(**item_dict)
            db.add(new_item)
            return new_item
        return self.router








