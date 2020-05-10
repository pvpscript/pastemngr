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
    
    user_op = parser.add_mutually_exclusive_group()
    user_op.add_argument(
            '--register',
            metavar='user',
            help='register a user in the local database'
    )
    user_op.add_argument(
            '--remove',
            metavar='user',
            help='remove a user from the local database'
    )

    subparsers = parser.add_subparsers(
            dest='command',
            help='subparser helperino'
    )

    ## register
    #register_parser = subparsers.add_parser(
    #        'register',
    #        help='register a user in the local database'
    #)
    #register_parser.add_argument(
    #        '--username',
    #        required=True,
    #        help='user to be registered on local database'
    #)

    ## remove
    #remove_user_parser = subparsers.add_parser(
    #        'remove',
    #        help='remove a user from the local database'
    #)
    #remove_user_parser.add_argument(
    #        '--username',
    #        required=True,
    #        help='user to be removed from local database'
    #)

    # user_info
    user_info_parser = subparsers.add_parser(
            'user_info',
            help='fetch information about an user.'
    )
    user_info_parser.add_argument(
            '--username',
            metavar='user',
            required=True,
            help='username to fetch info from'
    )
    user_info_parser.add_argument(
            '--local',
            action='store_true',
            help='get user info locally'
    )

    # new_paste
    new_paste_parser = subparsers.add_parser(
            'new_paste',
            help='create a new paste'
    )
    new_paste_parser.add_argument(
            '--username',
            metavar='user',
            help='username that owns the paste'
    )
    new_paste_parser.add_argument(
            '--name',
            metavar='name',
            help='paste title'
    )
    new_paste_parser.add_argument(
            '--format',
            metavar='fmt',
            choices=('text', 'c'),
            help='paste format'
    )
    new_paste_parser.add_argument(
            '--visibility',
            metavar='N',
            choices=('public', 'unlisted', 'private'),
            help='paste visibility'
    )
    new_paste_parser.add_argument(
            '--expire',
            metavar='time',
            choices=('5M', '10M'),
            help='paste expiration date'
    )

    # fetch_paste
    fetch_paste_parser = subparsers.add_parser(
            'fetch_paste',
            help='fetch a local paste or from pastebin'
    )
    fetch_paste_parser.add_argument(
            '--paste-key',
            metavar='key',
            required=True,
            help='paste to fetch'
    )
    fetch_paste_parser.add_argument(
            '--local',
            action='store_true',
            help='fetch paste locally'
    )

    # list_pastes
    list_parser = subparsers.add_parser(
            'list_pastes',
            help='list pastes from a user, locally or from pastebin'
    )
    list_parser.add_argument(
            '--username',
            metavar='user',
            required=True,
            help='user to list pastes from'
    )
    list_parser.add_argument(
            '--local',
            action='store_true',
            help='list pastes locally'
    )

    # delete_paste
    delete_parser = subparsers.add_parser(
            'delete',
            help='delete a paste from a user'
    )
    delete_parser.add_argument(
            '--username',
            metavar='user',
            required=True,
            help='paste owner'
    )
    delete_parser.add_argument(
            '--paste-id',
            metavar='id',
            required=True,
            help='paste id for deletion'
    )
    delete_parser.add_argument(
            '--local',
            help='also delete locally'
    )

    # paste_info
    paste_info_parser = subparsers.add_parser(
            'paste_info',
            help='''
            fetch information about a paste.
            This operation can only be done for pastes stored locally.
            '''
    )
    paste_info_parser.add_argument(
            '--paste-key',
            metavar='key',
            required=True,
            help='key of the paste to fetch information from'
    )

    # remove_expired
    rem_exp_parser = subparsers.add_parser(
            'remove_expired',
            help='remove local pastes that expired'
    )
    rem_exp_parser.add_argument(
            '--username',
            metavar='user',
            help='user to remove expired pastes from'
    )

    # update_db
    update_parser = subparsers.add_parser(
            'update_db',
            help='''
            update the local database for every registered
            user or for an individual user
            '''
    )
    update_parser.add_argument(
            '--username',
            metavar='user',
            help='user to be updated'
    )

    parser.parse_args()

#       dev_key = Config.read_dev_key()
#   
#       controller = c.Controller(dev_key)
#   #    controller.fetch_user_info(input('user: '), True if input('local: ') == 'true' else False)
#   
#   #    controller.list_user_pastes(input('user: '), True if input('local: ') == 'true' else False)
#       controller.remove_expired()
#       exit(0)
#       #controller.fetch_paste('S6AW24w0')
#       #exit(0)
#       #controller.purge_paste(input('username: '), 'CyESktB4')
#       #exit(0)
#       #controller.delete_paste(input('username: '), 'UZrcFQSB')
#       #exit(0)
#       controller.update_db()
#       exit(0)
#   
#       api_paste_code = input('text: ')
#       user_name = input('username: ')
#       api_paste_name = input('title: ')
#       api_paste_format = input('format: ')
#       api_paste_private = input('privacy level: ')
#   
#       controller.new_paste(api_paste_code, user_name if user_name != '' else None,
#               api_paste_name, api_paste_format, api_paste_private)
#   

#    user_key = user_controller.login()
#
#    print(user_key)

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
