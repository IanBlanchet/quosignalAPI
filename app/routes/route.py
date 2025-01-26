from fastapi import APIRouter

from app import schemas, models


router = APIRouter()

from app.routeFactory import RouteFactory

abonneRoute = RouteFactory('abonne', schemas.Abonne, schemas.BaseAbonne, models.Abonne, ['appels', 'contactUrgences'])
allAbonneRouter = abonneRoute.create_route_get_all()
abonneRouter = abonneRoute.create_route_get_item()
newAbonneRouter = abonneRoute.create_route_post_new(['heure', 'telephone'], ["modificateur"])

centreRoute = RouteFactory('centre', schemas.Centre, schemas.Centre, models.Centre, ['usagers', 'abonnes'])
centreRouter = centreRoute.create_route_get_item()
allCentreRouter = centreRoute.create_route_get_all()

usagerRoute = RouteFactory('usager', schemas.Usager, schemas.BaseUsager, models.Usager)
allUsagerRouter = usagerRoute.create_route_get_all()
usagerRouter = usagerRoute.create_route_get_item()
newUsagerRouter = usagerRoute.create_route_post_new(['email'], ["admin"])


appelRoute = RouteFactory('appel', schemas.Appel, schemas.BaseAppel, models.Appel)
allAppelRouter = appelRoute.create_route_get_all()
newAppelRouter = appelRoute.create_route_post_new([['date', 'abonne_id']])

contactUrgenceRoute = RouteFactory('contacturgence', schemas.ContactUrgence, schemas.BaseContactUrgence, models.ContactUrgence, ['abonnes'])
contactUrgenceRouter = contactUrgenceRoute.create_route_get_item()
newContactUrgence = contactUrgenceRoute.create_route_post_new([], ["modificateur"])

assAbonneContactUrgenceRoute = RouteFactory('ass_abonne_contacturgence', schemas.Ass_abonne_contactUrgence, schemas.BaseAss_abonne_contactUrgence, models.Ass_abonne_contactUrgence)
assAbonneContactUrgenceRouter = assAbonneContactUrgenceRoute.create_route_get_all()
assAbonneContactUrgenceRouter = assAbonneContactUrgenceRoute.create_route_post_new([['abonne_id', 'contactUrgence_id']])

