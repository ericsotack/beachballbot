import json

from flask import Response
from flask_restx import Namespace, Resource

from questions_core import questions as q
import questions_core as qc

api = Namespace("questions", description="Provides the ability to query for questions.")


# relative to defined namespace of /questions
@api.route("/")
class GetQuestions(Resource):
    def get(self):
        # returns the list of all questions {"questions: [q_list_elements]"}
        json_string = json.dumps({"questions": q.QuestionDB.sql_get_questions(qc.DATABASE_FILE)})
        return Response(json_string, content_type="application/json; charset=utf-8")


@api.route("/<int:idx>")
class GetQuestionsFromId(Resource):
    def get(self, idx):
        # get a question based on its id
        # returns {"question": [q]}
        json_string = json.dumps({"question": q.QuestionDB.sql_get_question_at_idx(idx, qc.DATABASE_FILE)})
        return Response(json_string, content_type="application/json; charset=utf-8")


@api.route("/random")
class GetQuestionsRandom(Resource):
    def get(self):
        json_string = json.dumps({"question": q.QuestionDB.sql_get_random_question(qc.DATABASE_FILE)})
        return Response(json_string, content_type="application/json; charset=utf-8")


@api.route("/size")
class GetSize(Resource):
    # returns the size of the list of questions {"size": int}
    def get(self):
        json_string = json.dumps({"size": q.QuestionDB.sql_size(qc.DATABASE_FILE)})
        return Response(json_string, content_type="application/json; charset=utf-8")
