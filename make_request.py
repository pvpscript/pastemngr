import re
import requests

BAD_REQUEST_STR = "Bad API request, "

class BadApiRequest(Exception):
    """ Raised when an API call returns an error """
    pass

def get():
    pass

def post(url, payload, parse_method):
    response = requests.post(url, payload).decode('utf-8')

    if bool(re.match(BAD_REQUEST_URL, response, re.I)):
        raise BadApiRequest(response[len(BAD_REQUEST_URL):])

    return parse_method(response)
