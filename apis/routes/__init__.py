from flask_restx import Api

from apis.routes.questions import api as questions_api
from apis.routes.groupme_bot import api as groupme_api


ALL_ROUTES = [questions_api, groupme_api]


# routes is a list of api objects to add
def init_app(app, routes):
    api = Api(
        title='Beach Ball API',
        version='1.0',
        description='Beach Ball API',
        doc='/doc/'
    )

    for route in routes:
        api.add_namespace(route)

    api.init_app(app)
