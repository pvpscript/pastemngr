import argparse

from config import Config
from pastebin_api import Pastebin
from make_request import post

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='tpastebin',
                                     description='Pastebin on terminal.')

    pastebin = Pastebin(Config.read_dev_key())


    login = input('login: ')
    passwd = input('password: ')

    user_key_data = pastebin.create_api_user_key(login, passwd)
    user_key = post(*user_key_data)
    
    print(user_key)
