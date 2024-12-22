from fastapi import Depends, FastAPI, HTTPException

from app.routes import AbonneRoute
from app.routes import CentreRoute

app = FastAPI()

app.include_router(AbonneRoute.router)
app.include_router(CentreRoute.router)
