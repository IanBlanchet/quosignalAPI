from fastapi import Depends, FastAPI

from app.routes import route

app = FastAPI()

app.include_router(route.allAbonneRouter)
app.include_router(route.newAbonneRouter)
app.include_router(route.abonneRouter)
app.include_router(route.allCentreRouter)
app.include_router(route.allUsagerRouter)
app.include_router(route.newUsagerRouter)
app.include_router(route.allAppelRouter)
app.include_router(route.newAppelRouter)