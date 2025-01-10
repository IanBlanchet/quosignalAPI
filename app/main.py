from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import route


app = FastAPI()

origins = [ "*" ] 



app.add_middleware( CORSMiddleware, 
                   allow_origins=origins, 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"], )




app.include_router(route.allAbonneRouter)
app.include_router(route.newAbonneRouter)
app.include_router(route.abonneRouter)
app.include_router(route.allCentreRouter)
app.include_router(route.allUsagerRouter)
app.include_router(route.newUsagerRouter)
app.include_router(route.allAppelRouter)
app.include_router(route.newAppelRouter)