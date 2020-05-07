import os
import argparse
from pastebin_api import Pastebin
from make_request import post

APP_NAME = 'tpastebin'

HOME = os.getenv('HOME')
XDG_CONFIG_HOME = os.getenv('XDG_CONFIG_HOME')

def read_dev_key(): 
    dev_key_file = HOME + '/.config/' + APP_NAME + '/dev_key' \
            if XDG_CONFIG_HOME == None \
            else XDG_CONFIG_HOME + '/' + APP_NAME + '/dev_key'

    file_ref = open(dev_key_file, 'r')

    dev_key = file_ref.readline().rstrip('\r\n')
    file_ref.close()

    return dev_key 



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=APP_NAME,
                                     description='Pastebin on terminal.')

    pastebin = Pastebin(read_dev_key())

    login = input('login: ')
    passwd = input('password: ')

    user_key_data = pastebin.create_api_user_key(login, passwd)
    user_key = post(*user_key_data)
    
    print(user_key)
