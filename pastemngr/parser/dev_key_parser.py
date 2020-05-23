import requests
import getpass

from html.parser import HTMLParser

import pastemngr
from pastemngr.core.config import Config

class KeyParserError(Exception):
    """An error occurred while obtaining the dev_key"""

class KeyParser(HTMLParser):
    __code_box = False
    __code_once = False
    __is_logged = False

    dev_key = None

    def handle_starttag(self, tag, attrs):
            for attr in attrs:
                    if (attr[0] == 'class' and attr[1] == 'code_box' and
                            not self.__code_once):
                        self.__code_box = True
                        self.__code_once = True
                    elif attr[0] == 'id' and attr[1] == 'header_members':
                        self.__is_logged = True

    def handle_data(self, data):
            if self.__code_box and self.__is_logged:
                    self.__code_box = False
                    self.dev_key = data

def fetch_dev_key(user_name):
    login_url = 'https://pastebin.com/login.php'
    api_page = 'https://pastebin.com/api'

    user_password = getpass.getpass('Password: ')

    payload = {
            'user_name': user_name,
            'user_password': user_password,
            'submit_hidden': 'submit_hidden'
    }

    try:
        with requests.Session() as s:
            s.post(login_url, data=payload)

            api_res = s.get(api_page)
    except requests.RequestException as e:
        raise KeyParserError

    parser = KeyParser()
    parser.feed(api_res.content.decode('UTF-8'))

    if parser.dev_key is not None:
        Config.write_dev_key(parser.dev_key)
    else:
        print('Unable to fetch dev key.')
