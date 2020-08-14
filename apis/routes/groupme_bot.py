import json
import os

import requests
from flask import Flask, g, request
from flask_restx import Namespace, Resource

from apis.routes import db
from questions_core import util
from questions_core import bot_helper as bh

POST_URL = "https://api.groupme.com/v3/bots/post"

CONFIG_FILE = str(util.get_project_root() / "data/groupme_config.json")

ENV_CONFIG = 'GROUPMECONF'

api = Namespace("groupme", description="Allows GroupMe to callback to a bot whenever a message is sent in a chat")


# CONFIG
# note that the owner of the bot needs to be in all of the groups that the bot is to be added to.

def read_in_config_file(conf_file):
    with open(conf_file) as cf:
        conf_str = cf.read()
    conf = json.loads(conf_str)
    return conf['bot_name'], conf['groups']


def read_in_config_env(env_var):
    conf_str = os.environ[env_var]
    print(conf_str)
    conf = json.loads(conf_str)
    return conf['bot_name'], conf['groups']


# SINGLETONS


def initial_setup(glob_vars):
    db.get_db()     # ensure db is initialized
    try:
        glob_vars.groupme_name, glob_vars.group_id_to_bot_id = read_in_config_file(CONFIG_FILE)
    except FileNotFoundError:
        glob_vars.groupme_name, glob_vars.group_id_to_bot_id = read_in_config_env(ENV_CONFIG)
    glob_vars.group_id_to_rqg = {}
    for group_id in glob_vars.group_id_to_bot_id:
        glob_vars.group_id_to_rqg[group_id] = bh.RandomQuestionGenerator(db.get_db())


def get_groupme_name():
    name = getattr(g, 'groupme_name', None)
    if name is None:
        initial_setup(g)
    return g.groupme_name


def get_bot_id(group_id):
    mapping = getattr(g, 'group_id_to_bot_id', None)
    if mapping is None:
        initial_setup(g)
    return g.group_id_to_bot_id[group_id]


def get_rqg(group_id) -> bh.RandomQuestionGenerator:
    mapping = getattr(g, 'group_id_to_rqg', None)
    if mapping is None:
        initial_setup(g)
    return g.group_id_to_rqg[group_id]


# APP


def init_app():
    app = Flask(__name__)
    # could do all of the initial setup stuff, but this gets handled when initial_setup() is called, when
    # any of the singletons are unfilled

    @app.before_request
    def before_request():
        initial_setup(g)

    return app


def send_message(msg, bot_id):
    data = {
        'bot_id': bot_id,
        'text': msg
    }
    requests.post(POST_URL, json=data)


# relative to defined namespace (see globals at top of file)
@api.route("/")
class GetQuestions(Resource):
    def post(self):
        data = request.get_json()

        # prevent bot from acting on its own messages
        if data['name'] != get_groupme_name() and data['text'] == ".ask":
            group_id = data['group_id']
            bot_id = get_bot_id(group_id)
            question = get_rqg(group_id).random_question()
            send_message(question, bot_id)

        return "ok", 200
