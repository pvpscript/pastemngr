import os
import argparse
import requests

APP_NAME = 'tpastebin'

HOME = os.getenv('HOME')
XDG_CONFIG_HOME = os.getenv('XDG_CONFIG_HOME')

POST_URL = 'https://pastebin.com/api/api_post.php'
LOGIN_URL = 'https://pastebin.com/api/api_login.php'
RAW_URL = 'https://pastebin.com/api/api_raw.php'

class Config():
    def __init__(self):
        self._dev_key_file = HOME + '/.config/' + APP_NAME + '/dev_key' \
                if XDG_CONFIG_HOME == None \
                else XDG_CONFIG_HOME + '/' + APP_NAME + '/dev_key'

    def read_dev_key(self): 
        file_ref = open(self._dev_key_file, 'r')

        self._dev_key = file_ref.readline().rstrip('\r\n')
        file_ref.close()

        return self._dev_key 



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=APP_NAME,
                                     description='Pastebin on terminal.')
    
    conf = Config()

    print(conf.read_dev_key())


