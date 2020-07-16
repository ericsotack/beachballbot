"""
Backend to read in a store of questions and offer a random question when queried.
"""

import json
import random
import time
import pyllist


""" Default location of the questions JSON file """
QUESTIONS = '../conf/questions.json'


class MostRecentQuestions(object):
    """
    Represents a queue of the most recent questions, so the most recently asked questions can be avoided.
    """
    def __init__(self, capacity=2):
        """
        Create a new MostRecentQuestions object.
        :param capacity: how many questions back should be avoided
        """
        self.llst = pyllist.dllist()
        self.capacity = capacity

    def clear(self):
        """
        Clears the current list of most recent questions
        :return: n/a
        """
        self.llst = pyllist.dllist()

    def add(self, question: str):
        """
        Adds a question to the list of most recent questions
        :param question: The question that was asked most recently
        :return: n/a
        """
        if self.llst.size < self.capacity:
            self.llst.append(question)
            self.capacity += 1
        else:   # at capacity
            self.llst.popleft()
            self.llst.append(question)

    def exists(self, question: str) -> bool:
        """
        Check if a question is present in the most recently asked questions
        :param question: The question to potentially be asked
        :return: True if the question was asked recently (within capacity history)
        """
        for node in self.llst.iternodes():
            if question == node():
                return True
        return False

    def size(self) -> int:
        """
        :return: The number of questions currently stored.
        """
        return self.llst.size


class QuestionDB(object):
    """
    Object that holds questions for use with a question chat bot.
    NOTE: The number of questions in a category must be greater than the capacity of the most recent.
    """

    def __init__(self, filename: str, capacity=2):
        """
        Read in a JSON data file containing an object mapping category types to arrays of
        questions relevant to that category.
        :param filename: Path to the json file in which the questions are stored.
        :return: A dictionary of question categories mapped to lists of relevant questions.
        """
        with open(filename) as fd:
            contents = fd.read()
        db = json.loads(contents)
        assert isinstance(db, dict)
        self.db = db
        self.mrq = MostRecentQuestions(capacity)

    def all_categories(self):
        """
        Return a list of all of the categories present in the database.
        :return: The categories of questions present
        """
        return self.db.keys()

    def questions_category(self, category: str) -> list:
        """
        From the question_db, gets the list of questions associated with a certain category
        :param category: The desired category of questions
        :return: The list of questions associated with that category
        """
        return self.db[category]

    def questions_categories(self, categories: list) -> list:
        """
        Get the list of questions associated with the list of
        :param categories: The list of categories to pull questions from
        :return: The list of questions associated with the given categories.
        """
        q_list = []
        for category in categories:
            q_list.extend(self.questions_category(category))
        return q_list

    def get_question(self, category: str = 'general') -> str:
        """
        Pull a random question from the specified category (general by default)
        :param category: The category to pull the question from.
        :return: A random question from the specified category
        """
        q_list = self.questions_category(category)
        return self.get_question_from_list(q_list)

    def get_question_from_list(self, q_list: list) -> str:
        """
        Pull a random question from a given list of questions.
        :param q_list: The list from which a random question is pulled.
        :return: A random question form the q_list
        """
        rand = random.Random()
        rand.seed(int(time.time()))
        cur = q_list[rand.randrange(len(q_list))]
        while self.mrq.exists(cur) and not self.mrq.size() < len(q_list):
            cur = q_list[rand.randrange(len(q_list))]
        self.mrq.add(cur)
        return cur
