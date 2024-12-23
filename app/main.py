from fastapi import Depends, FastAPI, HTTPException

from app.routes import AbonneRoute
from app.routes import CentreRoute
from app.routes import UsagerRoute
from app.routes import AppelRoute

app = FastAPI()

app.include_router(AbonneRoute.router)
app.include_router(CentreRoute.router)
app.include_router(UsagerRoute.router)
app.include_router(AppelRoute.router)
app.include_router(AbonneRoute.allAbonneRouter)
app.include_router(AbonneRoute.newAbonneRouter)