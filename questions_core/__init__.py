import sqlite3


""" Default location of the questions JSON file """
QUESTION_FILE = '../conf/questions.txt'

""" Default location of the questions sqlite db file """
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
            if not line.startswith('#'):    # comment out lines with #
                q_list.append(line.strip())
    return q_list


def create_db_from_list(q_list: list, db_file: str):
    """
    Creates a sqlite db at db_file containing the list of questions.
    :param q_list: The list of questions.
    :param db_file: The path to the file to store the sqlite db in.
    :return: n/a
    """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    try:
        cur.execute("DROP TABLE QUESTIONS")
    except sqlite3.OperationalError as err:
        print("WARNING", err)
    cur.execute("CREATE TABLE QUESTIONS ([qid] INTEGER PRIMARY KEY, [question] VARCHAR)")
    cur.executemany("INSERT INTO QUESTIONS (question) VALUES (?)", [(q,) for q in q_list])
    conn.commit()
    cur.close()


def init_app():
    q_list = read_config_file(QUESTION_FILE)
    create_db_from_list(q_list, DATABASE_FILE)
