import sys
import sqlite3

from config import Config

class Connect:
    __instance = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(self):
        if self.__instance == None:
            self.__instance = Connect()

        return self.__instance

    @classmethod
    def get_connection(self):
        connection = None

        try:
            url = Config.entry('tpastebin.db')

            connection = sqlite3.connect(url)
            connection.row_factory = sqlite3.Row
        except sqlite3.OperationalError:
            print("Couldn't connect to database.", file=sys.stderr)

        return connection



