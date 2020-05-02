import os
import argparse
import configparser
import requests

APP_NAME = 'tpastebin'

HOME = os.getenv('HOME')
XDG_CONFIG_HOME = os.getenv('XDG_CONFIG_HOME')

POST_URL = 'https://pastebin.com/api/api_post.php'
LOGIN_URL = 'https://pastebin.com/api/api_login.php'
RAW_URL = 'https://pastebin.com/api/api_raw.php'

class Config():
    def __init__(self):
        self.config = configparser.ConfigParser()

        self.config_file = HOME + '/.config/' + APP_NAME + '/config' \
                if XDG_CONFIG_HOME == None \
                else XDG_CONFIG_HOME + '/' + APP_NAME + '/config'

    def read_config(self): 
        self.config.read(self.config_file)

        self.api_key = self.config.get('API', 'KEY', raw=False)
        try:
            self.users = dict(self.config['USERS'])
        except KeyError:
            self.users = None
            
        return {'api_key': api_key, 'users': users}

class Pastebin():
    def __init__(self, config):
       pass 



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pastebin on terminal.')
    
    conf = Config()

    conf.read_config()


