from fastapi import Depends, FastAPI, HTTPException



from app.routes import AbonneRoute

app = FastAPI()

app.include_router(AbonneRoute.router)
