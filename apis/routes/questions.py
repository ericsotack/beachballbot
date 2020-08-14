import json

from flask import Response
from flask_restx import Namespace, Resource

from apis.routes.db import get_db


""" The API object that the /questions api is associated with """
api = Namespace("questions", description="Provides the ability to query for questions.")


# relative to defined namespace of /questions
@api.route("/")
class GetQuestions(Resource):
    """
    Class to handle requests to /questions
    """
    def get(self):
        """
        Method to handle requests for GET /questions
        :return: Response of JSON with the list of questions from the database.
        """
        # returns the list of all questions {"questions: [q_list_elements]"}
        json_string = json.dumps({"questions": get_db().questions()})
        return Response(json_string, content_type="application/json; charset=utf-8")


@api.route("/<int:idx>")
class GetQuestionsFromId(Resource):
    """
    Class to handle requests to /questions/<integer question idx>
    """
    def get(self, idx):
        """
        Method to handle requests for GET /questions/<idx of question>
        :param idx: The idx that was appended to the end of /questions/<idx>
        :return: Response of JSON with the question at the specified index.
        """
        # get a question based on its id
        # returns {"question": [q]}
        json_string = json.dumps({"question": get_db().question_at_index(idx)})
        return Response(json_string, content_type="application/json; charset=utf-8")


@api.route("/random")
class GetQuestionsRandom(Resource):
    """
    Class to handle requests to /questions/random
    """
    def get(self):
        """
        Method to handle requests for GET /questions/random for a random question.
        :return: Response of JSON with a random question.
        """
        json_string = json.dumps({"question": get_db().random_question()})
        return Response(json_string, content_type="application/json; charset=utf-8")


@api.route("/size")
class GetSize(Resource):
    """
    Class to handle requests to /questions/size
    """
    def get(self):
        """
        Method to handle requests for GET /questions/size for the number of available questions.
        :return: Response of JSON with the number of questions available in the database.
        """
        # returns the size of the list of questions {"size": int}
        json_string = json.dumps({"size": get_db().size()})
        return Response(json_string, content_type="application/json; charset=utf-8")
