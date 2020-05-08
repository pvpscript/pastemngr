import getpass as gp
import make_request as req
import database as db

from pastebin_api import Pastebin

class Controller:
    def __init__(self, dev_key):
        self.pastebin = Pastebin(dev_key)

        self.user = db.User()
        self.paste_info = db.PasteInfo()
        self.paste_text = db.PasteText()

    def __test_user_key(self, user_key):
        try:
            list_pastes_data = self.pastebin.list_user_pastes(user_key, 1)
            req.post(*list_pastes_data)
        except req.BadApiRequest:
            return False

        return True

    def login(self):
        username = input('Username: ')
        res = self.user.read(username)

        # if user doesn't exists, request login from api and put user in db
        if not res:
            passwd = gp.getpass('Password: ')

            user_key_data = self.pastebin.create_api_user_key(username, passwd)
            user_key = req.post(*user_key_data)['content']

            user_info_data = self.pastebin.fetch_user_info(user_key)
            user_info = req.post(*user_info_data)['content'][0]
            user_info = {**user_info, 'user_key': user_key}
            
            self.user.create(**user_info)

            return user_key

        # if user exists but has an invalid key, update key
        if not self.__test_user_key(res['user_key']):
            passwd = gp.getpass('Password: ')

            user_key_data = self.pastebin.create_api_user_key(username, passwd)
            user_key = req.post(*user_key_data)['content']

            self.user.update_key(username, user_key)

            return user_key

        return res['user_key']

# update_locally tells if the local database must be updated
# after a non local method execution.
#
# this option will be enabled by default.
#
# it can be disabled by setting an environment variable.
# PASTEBIN_UPDATE_LOCALLY = false
class UserController(Controller):
    def list_users(self):
        pass

    def register_user(self, user_name):
        pass

    # fetch user info from pastebin
    # if local is set to True, fetch locally instead
    def fetch_user_info(self, user_name, local=False): #update_locally
        pass

    def remove_user(self, user_name):
        pass

    # update local database for every registered user
    # if user_name is not None, update local database for specific user instead
    def update_db(self, user_name=None):
        pass

class PasteInfoController(Controller):
    # list pastes from pastebin
    # if local is True,  list only local pastes instead
    def list_user_pastes(self, user_name, local=False): #update_locally
        pass

    def new_paste(self, user_name): #update_locally
        pass

    # fetch paste info from pastebin
    # if local is True, fetch paste locally instead
    def fetch_paste_info(self, paste_key, local=False): #update_locally
        pass

    # delete paste from pastebin, but keep it locally
    def delete_paste(self, paste_key):
        pass

    # delete paste locally and from pastebin
    def purge_paste(self, paste_key):
        pass

    # remove expired from every registered user
    # if user_name is not None, remove expired from specific user instead
    def remove_expired(self, user_name=None):
        pass

class PasteTextController(Controller):
    # fetch paste from pastebin
    # if local is not False, fetch locally instead
    def fetch_paste(self, paste_key, local=False): #update_locally
        pass

# Might implement another time! (Table for local pastes only)
################################################################################
#class LocalPasteInfoController(Controller):
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
