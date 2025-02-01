from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import route
from app import auth

app = FastAPI()

origins = [ "*" ] 



app.add_middleware( CORSMiddleware, 
                   allow_origins=origins, 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"], )



app.include_router(auth.router)
#à l'importation de la première route, le router est auromatiquement loader pour le reste de route
app.include_router(route.allAbonneRouter)
app.include_router(route.allCentreRouter)
app.include_router(route.allUsagerRouter)
app.include_router(route.allAppelRouter)

