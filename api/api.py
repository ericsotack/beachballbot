from flask import Flask, g, jsonify
import questions as q
app = Flask(__name__)


@app.route('/questions', methods=['GET'])
def get_questions():
    # returns the list of all questions {"questions: [q_list_elements]"}
    return jsonify()


@app.route('/size', methods=['GET'])
def get_size():
    # returns the size of the list of questions {"size": int}
    pass


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
