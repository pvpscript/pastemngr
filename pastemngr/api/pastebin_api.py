import xml.etree.ElementTree as ET

POST_URL = 'https://pastebin.com/api/api_post.php'
LOGIN_URL = 'https://pastebin.com/api/api_login.php'
RAW_URL = 'https://pastebin.com/api/api_raw.php'
ANY_RAW_URL = 'https://pastebin.com/raw/' # this is not part of the API

def _output_string(val):
    return { 'content': val }

def _output_xml(val):
    root = ET.fromstring('<root>' + val + '</root>')

    ret_dict = {'content': []}
    for tag in root:
        tmp_dict = {}
        for e in tag:
            tmp_dict[e.tag] = e.text
        ret_dict['content'].append(tmp_dict)

    return ret_dict

class Pastebin():
    def __init__(self, dev_key):
        self.__dev_key = dev_key

    def create_api_user_key(self, api_user_name, api_user_password):
        payload = {
                'api_dev_key': self.__dev_key,
                'api_user_name': api_user_name,
                'api_user_password': api_user_password
        }

        return (LOGIN_URL, payload, _output_string)

    def create_paste(self, api_paste_code, api_user_key='',
                     api_paste_name='', api_paste_format='text',
                     api_paste_private='', api_paste_expire_date='N'):
        payload = {
                'api_dev_key': self.__dev_key,
                'api_option': 'paste',
                'api_paste_code': api_paste_code,
                'api_paste_name': api_paste_name,
                'api_user_key': api_user_key,
                'api_paste_format': api_paste_format,
                'api_paste_private': api_paste_private,
                'api_paste_expire_date': api_paste_expire_date
        }

        return (POST_URL, payload, _output_string)

    def list_user_pastes(self, api_user_key, api_results_limit=''):
        payload = {
                'api_dev_key': self.__dev_key,
                'api_option': 'list',
                'api_user_key': api_user_key,
                'api_results_limit': api_results_limit
        }

        return (POST_URL, payload, _output_xml)

    def delete_user_paste(self, api_user_key, api_paste_key):
        payload = {
                'api_dev_key': self.__dev_key,
                'api_option': 'delete',
                'api_user_key': api_user_key,
                'api_paste_key': api_paste_key
        }

        return (POST_URL, payload, _output_string)

    def fetch_user_info(self, api_user_key):
        payload = {
                'api_dev_key': self.__dev_key,
                'api_option': 'userdetails',
                'api_user_key': api_user_key
        }

        return (POST_URL, payload, _output_xml)

    def fetch_raw_paste(self, api_user_key, api_paste_key):
        payload = {
                'api_dev_key': self.__dev_key,
                'api_option': 'show_paste',
                'api_user_key': api_user_key,
                'api_paste_key': api_paste_key
        }

        return (RAW_URL, payload, _output_string)

    def fetch_any_raw_paste(self, api_paste_key):
        return (ANY_RAW_URL + api_paste_key, None, _output_string)
