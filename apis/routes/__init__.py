from flask_restx import Api

from apis.routes.questions import api as questions_api
from apis.routes.groupme_bot import api as groupme_api


""" Default list of apis to add to the passed in app """
ALL_ROUTES = [questions_api, groupme_api]


def init_app(app, routes):
    """
    Initialize the various routes.
    :param app: The app to initialize the routes in.
    :param routes: The list of flask api objects to add to the app.
    :return: n/a
    """
    api = Api(
        title='Beach Ball API',
        version='1.0',
        description='Beach Ball API',
        doc='/doc/'
    )

    for route in routes:
        api.add_namespace(route)

    api.init_app(app)
