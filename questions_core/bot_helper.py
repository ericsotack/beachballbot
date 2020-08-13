import threading
import time
import random

import questions_core.questions as q


class RandomQuestionGenerator(object):
    def __init__(self, questions: q.Questions, capacity=5):
        self.lock = threading.Lock()
        self.rand = random.Random()
        self.rand.seed(int(time.time()))
        self.questions = questions
        self.capacity = capacity
        with self.lock:
            self.recent = []

    def _size(self):
        with self.lock:
            return len(self.recent)

    def _add(self, item):
        with self.lock:
            if len(self.recent) < self.capacity:
                self.recent.append(item)
                self.capacity += 1
            else:
                self.recent.pop(0)
                self.recent.append(item)

    def _clear(self):
        with self.lock:
            self.recent = []

    def _is_recent(self, idx):
        with self.lock:
            return idx in self.recent

    def random_question(self) -> str:
        # avoids not having any question that can be asked
        if self._size() >= self.questions.size():
            self._clear()

        all_list = range(self.questions.size())     # all available indices in the db
        q_list = [idx for idx in all_list if not self._is_recent(idx)]  # difference between all_list and self.recent
        rand_idx = self.rand.randrange(len(q_list))     # the index in q_list that contains the db index to use
        return self.questions.question_at_index(q_list[rand_idx])
