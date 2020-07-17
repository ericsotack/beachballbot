"""
Backend to read in a store of questions and offer a random question when queried.
"""

import random
import time
import sqlite3

""" Default location of the questions JSON file """
QUESTION_FILE = '../conf/questions.txt'

DATABASE_FILE = '../conf/questions.db'


def read_config_file(filename: str) -> list:
    """
    filename should point to a file that has questions, each on its own line
    :param filename: The file from which to read the questions.
    :return: List of question strings.
    """
    q_list = []
    with open(filename) as fd:
        for line in fd.readlines():
            q_list.append(line.strip())
    return q_list


class QuestionDB(object):
    """
    Object that holds questions for use with a question chat bot.
    """

    def __init__(self, filename: str):
        """
        Read in a text data file containing the questions, each on its own line.
        :param filename: Path to the json file in which the questions are stored.
        :return: A list of question strings.
        """
        self.db = read_config_file(filename)
        self.rand = random.Random()
        self.rand.seed(time.time_ns())

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
        :return: A random question from the specified category
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
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("DROP TABLE QUESTIONS")
        cur.execute("CREATE TABLE QUESTIONS ([qid] INTEGER PRIMARY KEY, [question] VARCHAR)")
        cur.executemany("INSERT INTO QUESTIONS (question) VALUES (?)", [(q,) for q in self.db])
        conn.commit()
        cur.close()

    @staticmethod
    def sql_get_questions(db_file: str) -> list:
        """
        Get all questions from a sqlite database.
        :param db_file: The file that the sqlite db is stored in.
        :return: The question string at the specified index.
        """
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        val_lst = cur.execute("SELECT question FROM QUESTIONS").fetchall()
        conn.close()
        return [q for (q,) in val_lst]

    @staticmethod
    def sql_get_question_at_idx(idx: int, db_file: str) -> str:
        """
        Get the question at the 0-based index from a sqlite database.
        :param idx: The 0-based index for the question.
        :param db_file: The file that the sqlite db is stored in.
        :return: The question string at the specified index.
        """
        assert isinstance(idx, int)
        assert idx >= 0
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        # val_lst is list of row-tuples, sql table indexing starts at 1
        val_lst = cur.execute("SELECT question FROM QUESTIONS WHERE qid = ?", (idx + 1,)).fetchall()
        if len(val_lst) == 0:
            val = None
        else:
            val = val_lst[0][0]     # unpack singleton list of row-tuple from val_lst
        conn.close()
        return val

    @staticmethod
    def sql_get_random_question(db_file: str, omit_list = None) -> str:
        all_list = QuestionDB.sql_get_questions(db_file)

        if omit_list is None or len(omit_list) >= len(all_list):
            omit_list = []

        # difference between db_list and omit_list
        q_list = [item for item in all_list if item not in omit_list]

        rand = random.random()
        rand.seed(time.time_ns())
        idx = rand.randrange(len(q_list))
        return q_list[idx]


def debug():
    """
    Method to use when running this module directly.
    Allows for setting up debug scenarios
    :return: n/a
    """
    db = QuestionDB(QUESTION_FILE)
    print(db.db)
    # print(db.get_question())
    # print(db.get_question())
    #
    # denylist = read_config_file(QUESTION_FILE)
    # denylist = denylist[1:]
    # print(db.get_question(denylist))
    # print(db.get_question(denylist))
    db.sqlite_db(DATABASE_FILE)
    print(db.sql_get_question_at_idx(0, DATABASE_FILE))
    print(db.sql_get_questions(DATABASE_FILE))
    print(db.sql_get_random_question(DATABASE_FILE))


if __name__ == "__main__":
    debug()
