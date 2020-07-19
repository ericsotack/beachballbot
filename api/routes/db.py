from flask import g

import questions_core.util as qcutil
from questions_core.questions import QuestionsDB

FLASK_DATABASE_FILE = qcutil.DATABASE_FILE
FLASK_QUESTIONS_FILE = qcutil.QUESTION_FILE


# singleton db
def get_db():
    db = getattr(g, 'questions', None)
    if db is None:
        db = g.questions = QuestionsDB(FLASK_DATABASE_FILE)
    return db
