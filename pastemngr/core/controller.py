import os
import sys
import time
import tempfile

import getpass as gp

from subprocess import call

import pastemngr
import pastemngr.api.make_request as req
import pastemngr.db.database as db

from pastemngr.api.pastebin_api import Pastebin

class ControlError(Exception):
    """ An ambiguous error occurred during a controller execution """

    def __init__(self, msg, orig_exception):
        super(ControlError, self).__init__(f'{msg}: {orig_exception}')
        self.orig_exception = orig_exception

class OperationFailedError(ControlError):
    """ An error occurred during a control operation """

class PasteError(ControlError):
    """ An error occurred when trying to create a paste """

class EmptyContentError(PasteError):
    """ raised when trying to create a paste with empty content """

class EmptyFileError(PasteError):
    """ File provided was empty """


class Controller:
    def __init__(self, dev_key):
        self.pastebin = Pastebin(dev_key)

        self.user = db.User()
        self.paste_info = db.PasteInfo()
        self.paste_text = db.PasteText()

    def __read_from_editor(self):
        editor = os.environ.get('EDITOR', 'nano')
       
        #message = b'# Write your paste content. (this line will be ignored)'

        with tempfile.NamedTemporaryFile(suffix='.tmp') as tf:
            #tf.write(message)
            #tf.flush()
            call([editor, tf.name])

            #tf.seek(len(message)+1)

            content = tf.read()

            return content if content != b'' else None

    def __test_user_key(self, user_key):
        try:
            list_pastes_data = self.pastebin.list_user_pastes(user_key, 1)
            req.post(*list_pastes_data)
        except req.BadApiRequestError:
            return False

        return True

    def __login(self, user_name):
        res = self.user.read(user_name)

        # if user doesn't exists, request login from api and put user in db
        if not res:
            passwd = gp.getpass('Password: ')

            user_key_data = self.pastebin.create_api_user_key(
                    user_name,
                    passwd
            )
            user_key = req.post(*user_key_data)['content']

            user_info_data = self.pastebin.fetch_user_info(user_key)
            user_info = req.post(*user_info_data)['content'][0]
            user_info = {**user_info, 'user_key': user_key}
            
            self.user.create(**user_info)

            return user_key

        # if user exists but has an invalid key, update key
        if not self.__test_user_key(res['user_key']):
            passwd = gp.getpass('Password: ')

            user_key_data = self.pastebin.create_api_user_key(
                    user_name,
                    passwd
            )
            user_key = req.post(*user_key_data)['content']

            self.user.update_key(user_name, user_key)

            return user_key

        return res['user_key']

    def list_users(self, raw=False):
        try:
            users = self.user.all()

            if users is not None:
                if not raw:
                    print('\n---------- Registered users ----------')
                for u in users:
                    print(f'-> {u["user_name"]}')
                if not raw:
                    print('----------------------------------------')
            elif raw:
                print('There are no registered users')
        except db.DatabaseError as e:
            raise OperationFailedError('Couldn\'t list users', e)

    def register_user(self, user_name):
        try:
            res = self.user.read(user_name)
        except db.ReadError:
            res = False

        try:
            if not res:
                passwd = gp.getpass('Password: ')

                user_key_data = self.pastebin.create_api_user_key(
                        user_name,
                        passwd
                )
                user_key = req.post(*user_key_data)['content']

                user_info_data = self.pastebin.fetch_user_info(user_key)
                user_info = req.post(*user_info_data)['content'][0]
                user_info = {**user_info, 'user_key': user_key}
                
                if self.user.create(**user_info) == 1:
                    print('User succesfully registered')
        except (db.DatabaseError, req.BadApiRequestError) as e:
            raise ControlError('Couldn\'t register new user', e)

    # fetch user info from pastebin
    # if local is set to True, fetch locally instead
    def fetch_user_info(self, user_name, local=False, raw=False): #update_locally
        try:
            if local:
                user_info = self.user.read(user_name)
            else:
                user_info_data = self.pastebin.fetch_user_info(self.__login(user_name))
                user_info = req.post(*user_info_data)['content'][0]

            if user_info is not None:
                if not raw:
                    print('\n' + '{:-^80}'.format(''))
                    print('{:-^80}'.format(f' Information about the user [{user_name}] '))
                    print('{:-^80}'.format(''))
                for k, v in user_info.items():
                    print(f'{k}: {v}')
                if not raw:
                    print('{:-^80}'.format(''))
            else:
                print(f'\nThere are no records for user [{user_name}]')
        except (db.DatabaseError, req.BadApiRequestError) as e:
            raise OperationFailedError('Couldn\'t fetch user info', e)

    def remove_user(self, user_name):
        try:
            if self.user.delete(user_name) == 1:
                print('User removed successfully.')
            else:
                sys.stderr.write('Couldn\'t remove user or user is not registered.\n')
        except db.DatabaseError as e:
            raise OperationFailedError('Couldn\'t remove user.', e)

    # update local database for every registered user
    # if user_name is not None, update local database for specific user instead
    def update_db(self, user_name=None):
        try:
            updated_rows = 0
            created_rows = 0

            users = (
                    self.user.all()
                    if user_name is None 
                    else [{'user_name': user_name}]
            )

            for u in users:
                user_name = u['user_name']
                user_key = self.__login(user_name)

                user_info_data = self.pastebin.fetch_user_info(user_key)
                user_info = req.post(*user_info_data)['content'][0]
                updated_rows += self.user.update(**user_info)

                pastes_data = self.pastebin.list_user_pastes(user_key)
                pastes = req.post(*pastes_data)['content']

                for p in pastes:
                    paste_key = p['paste_key'] 

                    if self.paste_info.read(paste_key) is not None:
                        updated_rows += self.paste_info.update(**p)
                    else:
                        p = {**p, 'owner': user_name}
                        created_rows += self.paste_info.create(**p)

                        raw_paste_data = self.pastebin.fetch_raw_paste(
                                user_key,
                                paste_key
                        )
                        raw_paste = req.post(*raw_paste_data)['content']

                        created_rows += self.paste_text.create(
                                paste_key,
                                raw_paste
                        )
                            
            print(f'{updated_rows} rows updated')
            print(f'{created_rows} rows created')
        except db.DatabaseError as e:
            raise OperationFailedError('Unable to update database', e)

    # list pastes from pastebin
    # if local is True,  list only local pastes instead
    def list_user_pastes(self, user_name, local=False, raw=False):
        try:
            if local:
                pastes = self.user.list_user_pastes(user_name)
            else:
                user_key = self.__login(user_name)

                pastes_data = self.pastebin.list_user_pastes(user_key)
                pastes = req.post(*pastes_data)['content']

            for p in pastes:
                if not raw:
                    print('\n' + '{:-^80}'.format(''))
                for k, v in p.items():
                    print(f'{k}: {v}')
                if not raw:
                    print('{:-^80}'.format(''))
        except (db.DatabaseError, req.BadApiRequestError) as e:
            raise ControlError('Couldn\'t list user pastes', e)

    def new_paste(self, input_file=None, user_name=None, api_paste_name='',
                  api_paste_format='text', api_paste_private='',
                  api_paste_expire_date='N'):
        user_key = self.__login(user_name) if user_name is not None else ''
        api_paste_code = ''

        try:
            if input_file is not None:
                with open(input_file) as f:
                    api_paste_code = f.read()
                    if api_paste_code == '':
                        raise EmptyFileError('Paste file has no content.')
            else:
                api_paste_code = self.__read_from_editor()
                if api_paste_code is None:
                    raise EmptyContentError('Paste content is empty.')

            new_paste_data = self.pastebin.create_paste(
                    api_paste_code,
                    user_key,
                    api_paste_name,
                    api_paste_format,
                    api_paste_private,
                    api_paste_expire_date
            )
            new_paste = req.post(*new_paste_data)

            print(new_paste['content'])
        except (req.BadApiRequestError, FileNotFoundError) as e:
            raise OperationFailedError('Couldn\'t create paste', e)

    # fetch paste info locally
    def fetch_paste_info(self, paste_key):
        try:
            paste_info = self.paste_info.read(paste_key)

            for k, v in paste_info.items():
                print(f'{k}: {v}')
        except db.DatabaseError as e:
            raise OperationFailedError('Couldn\'t fetch paste info', e)
        
    # delete paste from pastebin, but keep it locally
    def delete_paste(self, user_name, paste_key):
        try:
            user_key = self.__login(user_name)

            del_paste_data = self.pastebin.delete_user_paste(user_key, paste_key)
            del_paste = req.post(*del_paste_data)

            print(del_paste['content'])
        except (req.BadApiRequestError, db.DatabaseError) as e:
            raise OperationFailedError('Couldn\'t delete paste', e)

    # delete paste locally and from pastebin
    def purge_paste(self, user_name, paste_key):
        try:
            user_key = self.__login(user_name)

            del_paste_data = self.pastebin.delete_user_paste(user_key, paste_key)
            del_paste = req.post(*del_paste_data)

            if self.paste_info.delete(paste_key) == 1:
                print('Successfully removed from local database')
            else:
                sys.stderr.write('Couldn\'t remove paste from local database or paste not found\n')

            print(del_paste['content'])
        except (req.BadApiRequestError, db.DatabaseError) as e:
            raise OperationFailedError('Couldn\'t purge paste', e)

    # remove expired from every registered user
    # if user_name is not None, remove expired from specific user instead
    def remove_expired(self, user_name=None):
        try:
            users = self.user.all()
            curr_time = time.time()

            removed = 0

            for u in users:
                user_name = u['user_name']
                pastes = self.user.list_user_pastes(user_name)

                for p in pastes:
                    expire_date = int(p['paste_expire_date'])
                    if expire_date > 0 and curr_time > expire_date:
                            removed += self.paste_info.delete(p['paste_key'])

            print(f'{removed} expired pastes removed')
        except db.DatabaseError as e:
            raise OperationFailedError('Couldn\'t remove expired pastes', e)

    # fetch paste from pastebin
    # if local is not False, fetch locally instead
    def fetch_paste(self, paste_key, local=False):
        try:
            if local:
                paste = self.paste_text.read(paste_key)['paste']
            else:
                paste_data = self.pastebin.fetch_any_raw_paste(paste_key)
                paste = req.post(*paste_data)['content']

            print(paste)
        except (req.BadApiRequestError, db.DatabaseError) as e:
            raise OperationFailedError('Couldn\'t fetch paste', e)


# Might implement another time! (Table for local pastes only)
################################################################################
# local_paste_info
#    def new_local_paste(self, user_name):
#        pass
#
#    def upload_local_paste(self, paste_id):
#        pass
#
#    def remove_local_paste(self, paste_id):
#        pass
#
################################################################################
