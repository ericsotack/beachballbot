from flask import Flask, g, jsonify
from flask.cli import with_appcontext

import questions as q
import click


# TODO  how to either instantiate a QuestionsDB to be used by all routes or
#       OR
# TODO  run the methods to create a db at startup so it can be referenced by file in routes


def init_app(appl):
    appl.teardown_appcontext(close_db)
    appl.cli.add_command(init_db_command())


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def init_db():
    db_file = get_db()
    q.QuestionDB.create_db(q.QUESTION_FILE, db_file)


def get_db():
    if 'db_file' not in g:
        g.db_file = q.DATABASE_FILE     # using this when it has a ../ is kinda sketchy
    return g.db_file


def close_db(e=None):
    db = g.pop('db', None)
    # if using sqlite, and altered it so the connection doesn't close?
    # if db is not None:
    #     db.close()


# TODO move this somewhere else
app = Flask(__name__)
init_app(app)


@app.route('/size', methods=['GET'])
def get_size():
    # returns the size of the list of questions {"size": int}
    pass


@app.route('/questions', methods=['GET'])
def get_questions():
    # returns the list of all questions {"questions: [q_list_elements]"}
    return jsonify()


@app.route('/questions/<int:qid>', methods=['GET'])
def get_question_from_id(qid):
    # get a question based on its id
    # returns {"question": []}
    pass


@app.route('/random', methods=['GET'])
def get_question_random():
    # return a random question
    pass


if __name__ == '__main__':
    app.run()
