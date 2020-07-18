from flask_restx import Api
from api.routes.questions import api as questions_api


ROUTES = [questions_api]


def init_app(app):
    api = Api(
        title='Beach Ball API',
        version='1.0',
        description='Beach Ball API',
        doc='/doc/'
    )

    for route in ROUTES:
        api.add_namespace(route)

    api.init_app(app)
