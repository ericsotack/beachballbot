from flask import Flask, g
from flask.cli import with_appcontext


import questions_core as qc
import api.routes as routes


def create_app():
    app = Flask(__name__)
    qc.init_app()
    routes.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
