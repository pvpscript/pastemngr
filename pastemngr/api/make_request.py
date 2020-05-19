import re
import requests

BAD_REQUEST_STR = "Bad API request, "

class BadApiRequestError(Exception):
    """ Raised when an API call returns an error """
    pass

def get():
    pass

def post(url, payload, parse_method):
    response = requests.post(url, payload).content.decode('UTF-8')

    if bool(re.match(BAD_REQUEST_STR, response, re.I)):
        raise BadApiRequestError(response[len(BAD_REQUEST_STR):])

    return parse_method(response)
