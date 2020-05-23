import re
import requests

BAD_REQUEST_STR = "Bad API request, "

class ApiError(Exception):
    """Ambiguous API error"""

    def __init__(self, msg, orig_exception):
        super().__init__(f'{msg}: {orig_exception}')
        self.orig_exception = orig_exception

class BadApiRequestError(Exception):
    """An API call returned an error"""

class ApiConnectionError(ApiError):
    """A Connection error occurred during the API request"""

class ApiTimeout(ApiError):
    """Api request timed out"""

def get():
    pass

def post(url, payload, parse_method):
    try:
        response = requests.post(url, payload).content.decode('UTF-8')

        if bool(re.match(BAD_REQUEST_STR, response, re.I)):
            raise BadApiRequestError(response[len(BAD_REQUEST_STR):])

        return parse_method(response)
    except requests.ConnectionError as e:
        raise ApiConnectionError('Couldn\'t connect', e)
    except requests.Timeout as e:
        raise ApiTimeout('Request timeout', e)

