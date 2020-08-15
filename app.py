from flask import Flask, make_response
from flask_talisman import Talisman

import questions_core as qc
import apis.routes as routes
import apis.routes.db as api_util


def create_app():
    flask_app = Flask(__name__, static_folder="./web", static_url_path='/')
    qc.init_db(q_file=api_util.FLASK_QUESTIONS_FILE, db_file=api_util.FLASK_DATABASE_FILE)

    # setup default routing to index.html
    @flask_app.route('/')
    def index():
        response = make_response(flask_app.send_static_file('index.html'))
        response.headers['Content-Security-Policy'] = "style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com"
        return response

    routes.init_app(flask_app, routes.ALL_ROUTES)

    return flask_app


app = create_app()
Talisman(app)


if __name__ == '__main__':
    app.run()
