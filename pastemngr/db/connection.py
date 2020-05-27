import os
import sys
import sqlite3

import pastemngr
from pastemngr.core.config import Config

class ConnectionError(Exception):
    """An error occurred during the database connection."""

class Connect:
    __connection = None 

    @classmethod
    def get_connection(self):
        if self.__connection is None:
            try:
                url = Config.entry('pastemngr.db')

                # Build database file, if it doesn't exist
                if not os.path.exists(url):
                    model = os.path.join(os.path.dirname(__file__), 'model.sql')

                    connection = sqlite3.connect(url)
                    model_file = open(model, 'r')
                    connection.executescript(model_file.read())
                else:
                    connection = sqlite3.connect(url)

                connection.row_factory = sqlite3.Row

                with connection as c:
                    cur = c.cursor()

                    cur.execute('PRAGMA foreign_keys = ON;')
            except sqlite3.OperationalError as e:
                raise ConnectionError

            self.__connection = connection
        
        return self.__connection
