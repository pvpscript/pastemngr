import argparse

from config import Config
from pastebin_api import Pastebin
from make_request import post

from database import User, PasteInfo, PasteText

import controller as c

from controller import Controller

import sys, tempfile, os

from dev_key_parser import fetch_dev_key

def format_args(args, drop_args):
    op_args = vars(args)
    
    for i in drop_args:
        del op_args[i]
    
    return op_args

def handle_args(args, drop_args):
    print(args)

    if args.fetch_dev_key:
        user_name = input('Username: ')
        fetch_dev_key(user_name)
        # Fix it for wrong logins
    else:
        dev_key = Config.read_dev_key()
        c = Controller(dev_key)

        method_table = {
                'list_users': c.list_users,
                'register': c.register_user,
                'remove': c.remove_user,
                'user_info': c.fetch_user_info,
                'new_paste': c.new_paste,
                'fetch_paste': c.fetch_paste,
                'list_pastes': c.list_user_pastes,
                'delete_paste': c.delete_paste,
                'purge_paste': c.purge_paste,
                'paste_info': c.fetch_paste_info,
                'remove_expired': c.remove_expired,
                'update_db': c.update_db
        }

        op = method_table[args.command]
        op_args = format_args(args, drop_args)

        #print('\n--------------------')
        #print(op)
        #print(op_args)

        op(**op_args)

        #print(args)

if __name__ == '__main__':
    drop_args = [] # arguments to be removed from the main arguments namespace

    parser = argparse.ArgumentParser(
            description='Pastebin on terminal.',
            epilog='A super helpful epilog',
    )
    main_arg = parser.add_argument(
            '--fetch-dev-key',
            action='store_true',
            help='fetch the developer key automatically and save it locally',
            dest='fetch_dev_key'
    )
    drop_args.append(main_arg.dest)

    subparsers = parser.add_subparsers(
            title='An interesting title',
            metavar='<command>',
            dest='command',
            help=''
    )
    drop_args.append(subparsers.dest)

    ## user_manage
    #register_parser = subparsers.add_parser(
    #        'user_manage',
    #        help='operations related to managing users in the local database'
    #)
    #user_op = user_manage_parser.add_mutually_exclusive_group()
    #user_op.add_argument(
    #        '--register',
    #        metavar='user',
    #        help='register a user in the local database'
    #)
    #user_op.add_argument(
    #        '--remove',
    #        metavar='user',
    #        help='remove a user from the local database'
    #)

    # register
    register_parser = subparsers.add_parser(
            'register',
            help='register a user in the local database'
    )
    register_parser.add_argument(
            '-u', '--username',
            metavar='USER',
            required=True,
            help='user to be registered on local database',
            dest='user_name'
    )

    # remove
    remove_user_parser = subparsers.add_parser(
            'remove',
            help='remove a user from the local database'
    )
    remove_user_parser.add_argument(
            '-u', '--username',
            metavar='USER',
            required=True,
            help='user to be removed from local database',
            dest='user_name'
    )

    # user_info
    user_info_parser = subparsers.add_parser(
            'user_info',
            help='fetch information about a user.'
    )
    user_info_parser.add_argument(
            '-u', '--username',
            metavar='USER',
            required=True,
            help='username to fetch info from',
            dest='user_name'
    )
    user_info_parser.add_argument(
            '--local',
            action='store_true',
            help='get user info locally',
            dest='local'
    )
    user_info_parser.add_argument(
            '--raw',
            action='store_true',
            help='print the output without fancy headers',
            dest='raw'
    )

    # new_paste
    new_paste_parser = subparsers.add_parser(
            'new_paste',
            help='create a new paste'
    )
    new_paste_parser.add_argument(
            '--input-file',
            metavar='FILE', 
            help='input file to upload as paste',
            dest='input_file'
    )
    new_paste_parser.add_argument(
            '-u', '--username',
            metavar='USER',
            help='username that owns the paste',
            dest='user_name'
    )
    new_paste_parser.add_argument(
            '--title',
            metavar='NAME',
            help='paste title',
            dest='api_paste_name'
    )
    new_paste_parser.add_argument(
            '--format',
            metavar='FMT',
            choices=('4cs', '6502acme', '6502kickass', '6502tasm', 'abap',
                'actionscript', 'actionscript3', 'ada', 'aimms', 'algol68',
                'apache', 'applescript', 'apt_sources', 'arduino', 'arm',
                'asm', 'asp', 'asymptote', 'autoconf', 'autohotkey', 'autoit',
                'avisynth', 'awk', 'bascomavr', 'bash', 'basic4gl', 'dos',
                'bibtex', 'blitzbasic', 'b3d', 'bmx', 'bnf', 'boo', 'bf', 'c',
                'c_winapi', 'c_mac', 'cil', 'csharp', 'cpp', 'cpp-winapi',
                'cpp-qt', 'c_loadrunner', 'caddcl', 'cadlisp', 'ceylon',
                'cfdg', 'chaiscript', 'chapel', 'clojure', 'klonec',
                'klonecpp', 'cmake', 'cobol', 'coffeescript', 'cfm', 'css',
                'cuesheet', 'd', 'dart', 'dcl', 'dcpu16', 'dcs', 'delphi',
                'oxygene', 'diff', 'div', 'dot', 'e', 'ezt', 'ecmascript',
                'eiffel', 'email', 'epc', 'erlang', 'euphoria', 'fsharp',
                'falcon', 'filemaker', 'fo', 'f1', 'fortran', 'freebasic',
                'freeswitch', 'gambas', 'gml', 'gdb', 'genero', 'genie',
                'gettext', 'go', 'groovy', 'gwbasic', 'haskell', 'haxe',
                'hicest', 'hq9plus', 'html4strict', 'html5', 'icon', 'idl',
                'ini', 'inno', 'intercal', 'io', 'ispfpanel', 'j', 'java',
                'java5', 'javascript', 'jcl', 'jquery', 'json', 'julia',
                'kixtart', 'kotlin', 'latex', 'ldif', 'lb', 'lsl2', 'lisp',
                'llvm', 'locobasic', 'logtalk', 'lolcode', 'lotusformulas',
                'lotusscript', 'lscript', 'lua', 'm68k', 'magiksf', 'make',
                'mapbasic', 'markdown', 'matlab', 'mirc', 'mmix', 'modula2',
                'modula3', '68000devpac', 'mpasm', 'mxml', 'mysql', 'nagios',
                'netrexx', 'newlisp', 'nginx', 'nim', 'text', 'nsis',
                'oberon2', 'objeck', 'objc', 'ocaml', 'ocaml-brief', 'octave',
                'oorexx', 'pf', 'glsl', 'oobas', 'oracle11', 'oracle8', 'oz',
                'parasail', 'parigp', 'pascal', 'pawn', 'pcre', 'per', 'perl',
                'perl6', 'php', 'php-brief', 'pic16', 'pike', 'pixelbender',
                'pli', 'plsql', 'postgresql', 'postscript', 'povray',
                'powerbuilder', 'powershell', 'proftpd', 'progress', 'prolog',
                'properties', 'providex', 'puppet', 'purebasic', 'pycon',
                'python', 'pys60', 'q', 'qbasic', 'qml', 'rsplus', 'racket',
                'rails', 'rbs', 'rebol', 'reg', 'rexx', 'robots', 'rpmspec',
                'ruby', 'gnuplot', 'rust', 'sas', 'scala', 'scheme', 'scilab',
                'scl', 'sdlbasic', 'smalltalk', 'smarty', 'spark', 'sparql',
                'sqf', 'sql', 'standardml', 'stonescript', 'sclang', 'swift',
                'systemverilog', 'tsql', 'tcl', 'teraterm', 'thinbasic',
                'typoscript', 'unicon', 'uscript', 'upc', 'urbi', 'vala',
                'vbnet', 'vbscript', 'vedit', 'verilog', 'vhdl', 'vim',
                'visualprolog', 'vb', 'visualfoxpro', 'whitespace', 'whois',
                'winbatch', 'xbasic', 'xml', 'xorg_conf', 'xpp', 'yaml',
                'z80', 'zxbasic'),
            help='paste format. (Check manual to see valid options)',
            dest='api_paste_format'
    )
    new_paste_parser.add_argument(
            '--visibility',
            metavar='N',
            choices=('0', '1', '2'),
            help='paste visibility. (%(choices)s)',
            dest='api_paste_private'
    )
    new_paste_parser.add_argument(
            '--expire',
            metavar='TIME',
            choices=('N', '10M', '1H', '1D', '1W', '2W', '1M', '6M', '1Y'),
            help='paste expiration date. (%(choices)s)',
            dest='api_paste_expire_date'
    )

    # fetch_paste
    fetch_paste_parser = subparsers.add_parser(
            'fetch_paste',
            help='fetch a paste\'s content'
    )
    fetch_paste_parser.add_argument(
            '--paste-key',
            metavar='KEY',
            required=True,
            help='paste to fetch',
            dest='paste_key'
    )
    fetch_paste_parser.add_argument(
            '--local',
            action='store_true',
            help='fetch paste locally',
            dest='local'
    )

    # list_pastes
    list_parser = subparsers.add_parser(
            'list_pastes',
            help='list pastes from a user'
    )
    list_parser.add_argument(
            '-u', '--username',
            metavar='USER',
            required=True,
            help='user to list pastes from',
            dest='user_name'
    )
    list_parser.add_argument(
            '--local',
            action='store_true',
            help='list pastes locally',
            dest='local'
    )
    list_parser.add_argument(
            '--raw',
            action='store_true',
            help='print the output without fancy headers',
            dest='raw'
    )

    # delete_paste
    delete_parser = subparsers.add_parser(
            'delete_paste',
            help='delete a paste from a user'
    )
    delete_parser.add_argument(
            '-u', '--username',
            metavar='USER',
            required=True,
            help='paste owner',
            dest='user_name'
    )
    delete_parser.add_argument(
            '--paste-key',
            metavar='KEY',
            required=True,
            help='paste id for deletion',
            dest='paste_key'
    )

    # purge_paste
    purge_parser = subparsers.add_parser(
            'purge_paste',
            help='delete a paste from a user (locally and from pastebin.com)'
    )
    purge_parser.add_argument(
            '-u', '--username',
            metavar='USER',
            required=True,
            help='paste owner',
            dest='user_name'
    )
    purge_parser.add_argument(
            '--paste-key',
            metavar='KEY',
            required=True,
            help='paste id for deletion',
            dest='paste_key'
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
            metavar='KEY',
            required=True,
            help='key of the paste to fetch information from',
            dest='paste_key'
    )

    # remove_expired
    rem_exp_parser = subparsers.add_parser(
            'remove_expired',
            help='remove local pastes that expired'
    )
    rem_exp_parser.add_argument(
            '-u', '--username',
            metavar='USER',
            help='user to remove expired pastes from',
            dest='user_name'
    )

    # list_users
    list_users_parser = subparsers.add_parser(
            'list_users',
            help='list registered users'
    )
    list_users_parser.add_argument(
            '--raw',
            action='store_true',
            help='print the output without fancy headers',
            dest='raw'
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
            '-u', '--username',
            metavar='USER',
            help='user to be updated',
            dest='user_name'
    )


    args = parser.parse_args()
    handle_args(args, drop_args)




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
