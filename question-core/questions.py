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
    NOTE: The number of questions in a category must be greater than the capacity of the most recent.
    """

    def __init__(self, filename: str):
        """
        Read in a text data file containing the questions, each on its own line.
        :param filename: Path to the json file in which the questions are stored.
        :return: A list of question strings.
        """
        self.db = read_config_file(filename)

    def get_question(self, omit_list=None) -> str:
        """
        Pull a random question (that does not appear in the ) from the question database.
        :param omit_list:
        :return: A random question from the specified category
        """
        if omit_list is None:
            omit_list = []
        rand = random.Random()
        rand.seed(int(time.time()))
        cur = self.db[rand.randrange(len(self.db))]
        while cur in omit_list:
            cur = self.db[rand.randrange(len(self.db))]
        return cur


def debug():
    """
    Method to use when running this module directly.
    Allows for setting up debug scenarios
    :return: n/a
    """
    db = QuestionDB(QUESTION_FILE)
    print(db.db)


if __name__ == "__main__":
    debug()
