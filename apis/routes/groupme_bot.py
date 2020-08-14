import json
import os

import requests
from flask import Flask, g, request
from flask_restx import Namespace, Resource

from apis.routes import db
from questions_core import util
from questions_core import bot_helper as bh

""" URL to post message sends back to """
POST_URL = "https://api.groupme.com/v3/bots/post"

""" Configuration file that contains the configuration for the groupme bot's name and groups """
CONFIG_FILE = str(util.get_project_root() / "data/groupme_config.json")

""" 
Environment variable with the JSON of the configuration for te groupme bot's name and groups. Alternative to
using the config_file
"""
ENV_CONFIG = 'GROUPMECONF'

""" The api that the groupme bot methods are a part of """
api = Namespace("groupme", description="Allows GroupMe to callback to a bot whenever a message is sent in a chat")


# CONFIG
# note that the owner of the bot needs to be in all of the groups that the bot is to be added to.

def read_in_config_file(conf_file):
    """
    Read in the JSON configuration file used to make the groupme bot aware of the groups it is in.
    :param conf_file: The path to the JSON file of configuration information for the groupme bot.
    :return: The bot_name from the config, the dictionary mapping group id to bot id for that group.
    """
    with open(conf_file) as cf:
        conf_str = cf.read()
    conf = json.loads(conf_str)
    return conf['bot_name'], conf['groups']


def read_in_config_env(env_var):
    """
    Read in the JSON configuration from an environment variable. Uses the JSON to make the groupme bot aware of the
    groups it is in.
    :param env_var: The name of the environment variable containing the JSON config file.
    :return: The bot_name from the config, the dictionary mapping group id to bot id for that group.
    """
    conf_str = os.environ[env_var]
    print(conf_str)
    conf = json.loads(conf_str)
    return conf['bot_name'], conf['groups']


# SINGLETONS


def initial_setup(glob_vars):
    """
    Initial setup for the groupme bot configuration. Given the global variable environment, fills in the values
    for the name and the dictionary mapping group_id to bot_id if they are missing.
    Attempts to read in the values from a JSON file and from an environment variable.
    Also verifies that the necessary sqlite database is present.
    :param glob_vars: The global variable environment where the values are to be stored.
    :return: n/a
    """
    db.get_db()     # ensure db is initialized
    try:
        glob_vars.groupme_name, glob_vars.group_id_to_bot_id = read_in_config_file(CONFIG_FILE)
    except FileNotFoundError:
        glob_vars.groupme_name, glob_vars.group_id_to_bot_id = read_in_config_env(ENV_CONFIG)
    glob_vars.group_id_to_rqg = {}
    for group_id in glob_vars.group_id_to_bot_id:
        glob_vars.group_id_to_rqg[group_id] = bh.RandomQuestionGenerator(db.get_db())


def get_groupme_name(glob_vars):
    """
    Get the groupme name from the global environment
    :param glob_vars: The global variable environment where the name is stored.
    :return: The name associated with the GroupMe bot.
    """
    name = getattr(glob_vars, 'groupme_name', None)
    if name is None:
        initial_setup(glob_vars)
    return glob_vars.groupme_name


def get_bot_id(glob_var, group_id):
    """
    Get the bot_id that identifies the bot in context as a member of a specific group.
    :param glob_var: The global variable environment where the name is stored.
    :param group_id: The group tha the bot is a member of that we want the specific bot_id for.
    :return: The bot_id for this bot associated with the specified group_id
    """
    mapping = getattr(glob_var, 'group_id_to_bot_id', None)
    if mapping is None:
        initial_setup(glob_var)
    return glob_var.group_id_to_bot_id[group_id]


def get_rqg(glob_var, group_id) -> bh.RandomQuestionGenerator:
    """
    Get the RandomQuestionGenrator for this specific group. Each group has their own RandomQuestionGenerator
    so they can manage their own state for what questions they have already seen.
    :param glob_var: The global variable environment where the name is stored.
    :param group_id: The group tha the bot is a member of that we want the specific RandomQuestionGenerator for.
    :return: The RandomQuestionGenerator object for that group.
    """
    mapping = getattr(glob_var, 'group_id_to_rqg', None)
    if mapping is None:
        initial_setup(glob_var)
    return glob_var.group_id_to_rqg[group_id]


# APP


def init_app():
    """
    Initialize the app. Setup the actions that occurs before a request, namely hat the global environment is
    verified to be ready.
    :return: The flask app.
    """
    app = Flask(__name__)

    @app.before_request
    def before_request():
        """
        Before a request is handled, ensure that the global environment is initialized.
        :return:
        """
        initial_setup(g)

    return app


def send_message(msg, bot_id):
    """
    POST a message back to the GroupMe API.
    :param msg: The text to send in the message.
    :param bot_id: The bot_id that identifies the bot and group that is sending the message.
    :return: n/a
    """
    data = {
        'bot_id': bot_id,
        'text': msg
    }
    requests.post(POST_URL, json=data)


# relative to defined namespace (see globals at top of file)
@api.route("/")
class GetQuestions(Resource):
    """
    Class to handle requests to /groupme
    """
    def post(self):
        """
        Method to handle requests for POST /groupme to notify the bot when a message is sent to a chat
        that it is a part of. If the message is a recognized command, respond to the command and send the
        response back to the originating group.
        :return: "ok" text string, success status code
        """
        data = request.get_json()

        # prevent bot from acting on its own messages
        if data['name'] != get_groupme_name(g) and data['text'] == ".ask":
            group_id = data['group_id']
            bot_id = get_bot_id(g, group_id)
            question = get_rqg(g, group_id).random_question()
            print("Question:", question)
            print("group_id:", group_id)
            print("bot_id", bot_id)
            send_message(question, bot_id)

        return "ok", 200
