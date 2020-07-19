from pathlib import Path


def get_project_root():
    """Returns project root folder."""
    return Path(__file__).parent.parent


""" Default location of the questions JSON file """
QUESTION_FILE = str(get_project_root() / 'data/questions.txt')

""" Default location of the questions sqlite db file """
DATABASE_FILE = str(get_project_root() / 'data/questions.db')