import json

from flask import Response
from flask_restx import Namespace, Resource

from apis.routes.db import get_db


api = Namespace("questions", description="Provides the ability to query for questions.")


# relative to defined namespace of /questions
@api.route("/")
class GetQuestions(Resource):
    def get(self):
        # returns the list of all questions {"questions: [q_list_elements]"}
        json_string = json.dumps({"questions": get_db().questions()})
        return Response(json_string, content_type="application/json; charset=utf-8")


@api.route("/<int:idx>")
class GetQuestionsFromId(Resource):
    def get(self, idx):
        # get a question based on its id
        # returns {"question": [q]}
        json_string = json.dumps({"question": get_db().question_at_index(idx)})
        return Response(json_string, content_type="application/json; charset=utf-8")


@api.route("/random")
class GetQuestionsRandom(Resource):
    def get(self):
        json_string = json.dumps({"question": get_db().random_question()})
        return Response(json_string, content_type="application/json; charset=utf-8")


@api.route("/size")
class GetSize(Resource):
    # returns the size of the list of questions {"size": int}
    def get(self):
        json_string = json.dumps({"size": get_db().size()})
        return Response(json_string, content_type="application/json; charset=utf-8")
