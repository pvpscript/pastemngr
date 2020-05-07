import argparse

from config import Config
from pastebin_api import Pastebin
from make_request import post

from database import User, PasteInfo, PasteText

import controller as c

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='tpastebin',
                                     description='Pastebin on terminal.')

    dev_key = Config.read_dev_key()

    user_controller = c.UserController(dev_key)
    user_key = user_controller.login()

    print(user_key)

    #user = User()
    #user.update(user_name='userino',
    #        user_key='updated_key_for_userino', user_format_short='text',
    #        user_expiration='N', user_avatar_url='www.new_avatar_url.com',
    #        user_private=0, user_website='www.my-new-website.com',
    #        user_email='myBrandNewEmail@provider.com',
    #        user_location='I just moved to a new location',
    #        user_account_type=1)
    #user.update_key(user_name='userino',
    #        user_key='some_Key')
    

    """
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
    """
