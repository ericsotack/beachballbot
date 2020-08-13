import json
import requests
from flask import Flask, g, request
from flask_restx import Namespace, Resource

from api.routes import db
from questions_core import util
from questions_core import bot_helper as bh

POST_URL = "https://api.groupme.com/v3/bots/post"

CONFIG_FILE = str(util.get_project_root() / "data/groupme_config.json")

api = Namespace("groupme", description="Allows GroupMe to callback to a bot whenever a message is sent in a chat")


# I think the owner of the bot needs to be in all of the groups that the bot is to be in.
# Figure out how to do automatic deployment of bots in many groups
#   figure out all of the group ids manually
#   manually send json requests to register the bot in each group
#       save the bot_id from each response and put them into the json file mapping from group id to bot id


# CONFIG


def read_in_config(conf_file):
    with open(conf_file) as cf:
        conf_str = cf.read()
    conf = json.loads(conf_str)
    return conf['bot_name'], conf['groups']


# SINGLETONS


def initial_setup():
    db.get_db()     # ensure db is initialized
    g.name, g.group_id_to_bot_id = read_in_config(CONFIG_FILE)
    g.group_id_to_rqg = {}
    for group_id in g.group_id_to_bot_id:
        g.group_id_to_rqg[group_id] = bh.RandomQuestionGenerator(db.get_db())


def get_groupme_name():
    name = getattr(g, 'groupme_name', None)
    if name is None:
        initial_setup()
    return g.groupme_name


def get_bot_id(group_id):
    mapping = getattr(g, 'group_id_to_bot_id', None)
    if mapping is None:
        initial_setup()
    return g.group_id_to_bot_id[group_id]


def get_rqg(group_id) -> bh.RandomQuestionGenerator:
    mapping = getattr(g, 'group_id_to_rqg', None)
    if mapping is None:
        initial_setup()
    return g.group_id_to_rqg[group_id]


# APP


def init_app():
    app = Flask(__name__)
    # could do all of the initial setup stuff, but this gets handled when initial_setup() is called, when
    # any of the singletons are unfilled
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
