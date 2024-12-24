from fastapi import APIRouter

from app import schemas, models


router = APIRouter()

from app.routeFactory import RouteFactory

abonneRoute = RouteFactory('abonne', schemas.Abonne, schemas.BaseAbonne, models.Abonne)
allAbonneRouter = abonneRoute.create_route_get_all()
newAbonneRouter = abonneRoute.create_route_post_new(['heure', 'telephone'])

centreRoute = RouteFactory('centre', schemas.Centre, schemas.Centre, models.Centre)
allCentreRouter = centreRoute.create_route_get_all()

usagerRoute = RouteFactory('usager', schemas.Usager, schemas.BaseUsager, models.Usager)
allUsagerRouter = usagerRoute.create_route_get_all()
newUsagerRouter = usagerRoute.create_route_post_new(['email'])

appelRoute = RouteFactory('appel', schemas.Appel, schemas.BaseAppel, models.Appel)
allAppelRouter = appelRoute.create_route_get_all()
newAppelRouter = appelRoute.create_route_post_new([['date', 'abonne']])
