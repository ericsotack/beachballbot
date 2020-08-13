from flask import Flask

import questions_core as qc
import apis.routes as routes
import apis.routes.db as api_util


def create_app():
    flask_app = Flask(__name__, static_folder="./web", static_url_path='/')
    qc.init_db(q_file=api_util.FLASK_QUESTIONS_FILE, db_file=api_util.FLASK_DATABASE_FILE)

    # setup default routing to index.html
    @flask_app.route('/')
    def index():
        return flask_app.send_static_file('index.html')

    routes.init_app(flask_app, routes.ALL_ROUTES)

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run()
