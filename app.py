from flask import Flask

import questions_core as qc
import api.routes as routes
import api.routes.db as api_util


def create_app():
    app = Flask(__name__)
    qc.init_db(q_file=api_util.FLASK_QUESTIONS_FILE, db_file=api_util.FLASK_DATABASE_FILE)
    routes.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
