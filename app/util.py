from fastapi import Depends, HTTPException


def fieldUniqueValidation(item_dict, fields, db, model):
    """permet de valider si un champ unique est déjà présent dans la bd

    Args:
        item_dict (schemas): le nouvel item soumis
        fields (str ou list): un champs ou une liste de champs qui doivent être unique
        db : la bd
        model (sqlAlchemy model): le model sql alchemy

    Raises:
        HTTPException: exception levée si le champ est déjà présent
        
    """
    for field in fields:
                if type(field) == list:
                    existItem = db.query(model).where(and_(getattr(model, field[0]) == item_dict[field[0]] , getattr(model, field[1]) == item_dict[field[1]])).first()
                    if existItem:
                        raise HTTPException(status_code=400, detail=f"La combinaison {field[0]} et {field[1]} existe déjà")
                else:
                    existItem = db.query(model).where(getattr(model, field) == item_dict[field]).first()
                    if existItem:
                        raise HTTPException(status_code=400, detail=f"{field} existe déjà")
    


