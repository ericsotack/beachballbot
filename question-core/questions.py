"""
Backend to read in a store of questions and offer a random question when queried.
"""

import random
import time


""" Default location of the questions JSON file """
QUESTION_FILE = '../conf/questions.txt'


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
        self.rand.seed(time.time())

    def get_question(self, omit_list=None) -> str:
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
        cur = self.db[idx]
        while cur in omit_list:
            idx = self.rand.randrange(len(q_list))
            cur = self.db[idx]
        return cur


def debug():
    """
    Method to use when running this module directly.
    Allows for setting up debug scenarios
    :return: n/a
    """
    db = QuestionDB(QUESTION_FILE)
    print(db.db)
    print(db.get_question())
    print(db.get_question())

    denylist = read_config_file(QUESTION_FILE)
    denylist = denylist[1:]
    print(db.get_question(denylist))
    print(db.get_question(denylist))


if __name__ == "__main__":
    debug()
