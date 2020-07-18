from flask_restx import Namespace, Resource

from questions_core import questions as q
import questions_core as qc

api = Namespace("questions", description="Provides the ability to query for questions.")


# relative to defined namespace
@api.route("/")
class GetQuestions(Resource):
    def get(self):
        # returns the list of all questions {"questions: [q_list_elements]"}
        return {"questions": q.QuestionDB.sql_get_questions(qc.DATABASE_FILE)}


@api.route("/<int:idx>")
class GetQuestionsFromId(Resource):
    def get(self, idx):
        # get a question based on its id
        # returns {"question": [q]}
        return {"question": q.QuestionDB.sql_get_question_at_idx(idx, qc.DATABASE_FILE)}


@api.route("/random")
class GetQuestionsRandom(Resource):
    def get(self):
        return {"question": q.QuestionDB.sql_get_random_question(qc.DATABASE_FILE)}


@api.route("/size")
class GetSize(Resource):
    # returns the size of the list of questions {"size": int}
    def get(self):
        return {"size": q.QuestionDB.sql_size(qc.DATABASE_FILE)}
