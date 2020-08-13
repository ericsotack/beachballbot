"""
Backend to read in a store of questions and offer a random question when queried.
"""

import random
import time
import sqlite3

import questions_core as qc
import questions_core.util as util


class Questions(object):    # informal interface bc i don't feel like figuring out the abc package
    def size(self):
        raise NotImplementedError

    def questions(self):
        raise NotImplementedError

    def question_at_index(self, idx: int):
        raise NotImplementedError

    def random_question(self, omit_list=None):
        raise NotImplementedError


class QuestionsList(Questions):
    """
    Object that holds questions for use with a question chat bot.
    Stores questions in a list.
    """

    def __init__(self, filename=util.QUESTION_FILE):
        """
        Read in a text data file containing the questions, each on its own line.
        :param filename: Path to the json file in which the questions are stored.
        :return: A list of question strings.
        """
        self.db = qc.read_config_file(filename)
        self.rand = random.Random()
        self.rand.seed(int(time.time()))

    def size(self):
        """
        :return: The number of questions available.
        """
        return len(self.db)

    def questions(self) -> list:
        """
        :return: List of all question strings
        """
        return self.db

    def question_at_index(self, idx: int) -> str:
        """
        :param idx: The index in the question list to get the question (must be < the length of question_list)
        :return: The question at the specified index.
        """
        assert idx < len(self.db)
        return self.db[idx]

    def random_question(self, omit_list=None) -> str:
        """
        Pull a random question (that does not appear in the omit_list) from the question database.
        :param omit_list: List of question strings to not produce.
        :return: A random question from the collection of questions.
        """
        # avoids not having any question that can be asked
        if omit_list is None or len(omit_list) >= len(self.db):
            omit_list = []
        # difference between db_list and omit_list
        q_list = [item for item in self.db if item not in omit_list]
        idx = self.rand.randrange(len(q_list))
        return q_list[idx]

    def sqlite_db(self, db_file: str):
        """
        Creates a sqlite db at db_file containing the list of questions.
        :param db_file: The path to the file to store the sqlite db in.
        :return: n/a
        """
        qc.create_db_from_list(self.db, db_file)


class QuestionsDB(Questions):
    """
    Object that holds questions for use with a question chat bot.
    Stores questions in a sqlite db.
    """
    def __init__(self, db_file):
        self.db_file = db_file
        qc.init_db()

    def size(self):
        """
        Determines how many questions are in the database
        :return: The number of questions in the database.
        """
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        val_lst = cur.execute("SELECT COUNT(*) FROM QUESTIONS").fetchall()
        conn.close()
        return val_lst[0][0]

    def questions(self):
        """
        Get all questions from a sqlite database.
        :return: The question string at the specified index.
        """
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        val_lst = cur.execute("SELECT question FROM QUESTIONS").fetchall()
        conn.close()
        return [q for (q,) in val_lst]

    def question_at_index(self, idx):
        """
        Get the question at the 0-based index from a sqlite database.
        :param idx: The 0-based index for the question.
        :return: The question string at the specified index.
        """
        assert isinstance(idx, int)
        assert idx >= 0
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        # val_lst is list of row-tuples, sql table indexing starts at 1
        val_lst = cur.execute("SELECT question FROM QUESTIONS WHERE qid = ?", (idx + 1,)).fetchall()
        if len(val_lst) == 0:
            val = None
        else:
            val = val_lst[0][0]     # unpack singleton list of row-tuple from val_lst
        conn.close()
        return val

    def random_question(self, omit_list=None) -> str:
        """
        Get a random question from a sqlite db.
        :param omit_list: List of question strings to not produce.
        :return: A random question from the collection of questions.
        """
        all_list = self.questions()

        if omit_list is None or len(omit_list) >= len(all_list):
            omit_list = []

        # difference between db_list and omit_list
        q_list = [item for item in all_list if item not in omit_list]

        rand = random.Random()
        rand.seed(int(time.time()))
        idx = rand.randrange(len(q_list))
        return q_list[idx]


def debug():
    """
    Method to use when running this module directly.
    Allows for setting up debug scenarios
    :return: n/a
    """
    db = QuestionsList(util.QUESTION_FILE)
    print(db.db)


if __name__ == "__main__":
    debug()
