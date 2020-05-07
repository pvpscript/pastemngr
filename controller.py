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

        if not self.__test_user_key(res['user_key']):
            passwd = gp.getpass('Password: ')

            user_key_data = self.pastebin.create_api_user_key(username, passwd)
            user_key = req.post(*user_key_data)['content']

            self.user.update_key(username, user_key)

            return user_key

        return res['user_key']

class UserController(Controller):
    pass

class PasteInfoController(Controller):
    pass

class PasteTextController(Controller):
    pass
