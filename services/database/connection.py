import sqlite3
from os import path
from sqlite3 import Error


def create_connection():
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(path.dirname(path.abspath(__file__)) + '/' + 'pythonsqlite.db')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
