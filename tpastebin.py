import argparse

from config import Config
from pastebin_api import Pastebin
from make_request import post

from database import User, PasteInfo, PasteText

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='tpastebin',
                                     description='Pastebin on terminal.')

    pastebin = Pastebin(Config.read_dev_key())


    login = input('login: ')
    passwd = input('password: ')


    user_key_data = pastebin.create_api_user_key(login, passwd)
    user_key = post(*user_key_data)

    user_pastes_data = pastebin.list_user_pastes(user_key['content'])
    user_pastes = post(*user_pastes_data)

    user_info_data = pastebin.fetch_user_info(user_key['content'])
    user_info = post(*user_info_data)

    print("\n---------- User key ----------")
    print(user_key)

    print("\n---------- User pastes ----------")
    print(user_pastes)

    print("\n---------- User info ----------")
    print(user_info)


    exit(0)

    user = User()
    print('Single read')
    print(user.read('userino'))
    print('\nReading all')
    print(user.all())

    print('\n\n')

    paste_info = PasteInfo()
    print('Single read')
    print(paste_info.read('key_123'))
    print('\nReading all')
    print(paste_info.all())

    print('\n\n')

    paste_text = PasteText()
    print('Single read')
    print(paste_text.read('key_123'))
    print('\nReading all')
    print(paste_text.all())

    print(paste_text.read('lmao'))
    
