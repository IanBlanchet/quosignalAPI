from fastapi import APIRouter

from app import schemas, models


router = APIRouter()

from app.routeFactory import RouteFactory

abonneRoute = RouteFactory('abonne', schemas.Abonne, schemas.BaseAbonne, models.Abonne, ['appels', 'contactUrgences'])
allAbonneRouter = abonneRoute.create_route_get_all(['benevole'])
abonneRouter = abonneRoute.create_route_get_item(['benevole'])
newAbonneRouter = abonneRoute.create_route_post_new(['heure', 'telephone'], ["modificateur"])

centreRoute = RouteFactory('centre', schemas.Centre, schemas.Centre, models.Centre, ['usagers', 'abonnes'])
centreRouter = centreRoute.create_route_get_item(['benevole'])
allCentreRouter = centreRoute.create_route_get_all(['benevole'])

usagerRoute = RouteFactory('usager', schemas.Usager, schemas.BaseUsager, models.Usager)
allUsagerRouter = usagerRoute.create_route_get_all(['modificateur'])
usagerRouter = usagerRoute.create_route_get_item(['modificateur'])
editUsagerRouter = usagerRoute.create_route_edit_item(['email'], ["admin"])


appelRoute = RouteFactory('appel', schemas.Appel, schemas.BaseAppel, models.Appel)
allAppelRouter = appelRoute.create_route_get_all(['benevole'])
newAppelRouter = appelRoute.create_route_post_new([['date', 'abonne_id']])

contactUrgenceRoute = RouteFactory('contacturgence', schemas.ContactUrgence, schemas.BaseContactUrgence, models.ContactUrgence, ['abonnes'])
contactUrgenceRouter = contactUrgenceRoute.create_route_get_item(['benevole'])
newContactUrgence = contactUrgenceRoute.create_route_post_new([], ["modificateur"])

assAbonneContactUrgenceRoute = RouteFactory('ass_abonne_contacturgence', schemas.Ass_abonne_contactUrgence, schemas.BaseAss_abonne_contactUrgence, models.Ass_abonne_contactUrgence)
assAbonneContactUrgenceRouter = assAbonneContactUrgenceRoute.create_route_get_all(['benevole'])
assAbonneContactUrgenceRouter = assAbonneContactUrgenceRoute.create_route_post_new([['abonne_id', 'contactUrgence_id']])

