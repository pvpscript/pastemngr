import argparse

from config import Config
from pastebin_api import Pastebin
from make_request import post

from database import User, PasteInfo, PasteText

import controller as c

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Pastebin on terminal.',
            epilog='A super helpful epilog',
    )
    subparsers = parser.add_subparsers(dest='command',
                                      help='subparser helperino')

    # register
    register_parser = subparsers.add_parser('register', help='register help')
    register_parser.add_argument('--username', required=True,
                                 help='user to be registered on local database')

    # remove
    remove_user_parser = subparsers.add_parser('remove', help='remove help')
    remove_user_parser.add_argument('--username', required=True,
                                    help='user to be removed from local database')

    # user_info
    user_info_parser = subparsers.add_parser('user_info', help='user_info help')
    user_info_parser.add_argument('--username', required=True,
                                  help='username to fetch info from')
    user_info_parser.add_argument('--local', help='get user info locally')

    # new_paste
    new_paste_parser = subparsers.add_parser('new_paste', help='new_paste help')
    new_paste_parser.add_argument('--username', help='username help')
    new_paste_parser.add_argument('--name', help='paste title')
    new_paste_parser.add_argument('--format',
                                  choices=('text', 'c'),
                                  help='paste format')
    new_paste_parser.add_argument('--visibility',
                                  choices=('public', 'unlisted', 'private'),
                                  help='paste visibility')
    new_paste_parser.add_argument('--expire',
                                  choices=('5M', '10M'),
                                  help='paste expiration date')


    # fetch_paste
    fetch_paste_parser = subparsers.add_parser('fetch_paste', help='fetch_paste help')
    fetch_paste_parser.add_argument('--paste-key', required=True,
                                    help='paste to fetch')
    fetch_paste_parser.add_argument('--local', help='fetch paste locally')

    # list_pastes
    list_parser = subparsers.add_parser('list_pastes', help='list_pastes help')
    list_parser.add_argument('--username', required=True,
                             help='list user pastes')
    list_parser.add_argument('--local', help='list pastes locally')

    # delete_paste
    list_parser = subparsers.add_parser('delete', help='list help')
    list_parser.add_argument('--username', required=True,
                             help='paste owner')
    list_parser.add_argument('--paste-id', required=True,
                             help='paste id for deletion')
    list_parser.add_argument('--local', help='also delete locally')

    # paste_info
    paste_info_parser = subparsers.add_parser('paste_info', help='paste_info help')
    paste_info_parser.add_argument('--paste-key', required=True,
                                   help='key of the paste to fetch information from')
    paste_info_parser.add_argument('--local', help='fetch information locally')

    # remove_expired
    rem_exp_parser = subparsers.add_parser('remove_expired', help='remove_expired help')
    rem_exp_parser.add_argument('--username',
                                help='user to remove expired pastes from')

    # update_db
    update_parser = subparsers.add_parser('update_db', help='upadte_db help')
    update_parser.add_argument('--username',
                               help='update for specific user only')

    parser.parse_args()

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
