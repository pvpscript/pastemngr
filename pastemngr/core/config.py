import os

class DevKeyNotFoundError(FileNotFoundError):
    """ Dev key file not found """

    def __init__(self, msg, orig_exception):
        super().__init__(f'{msg}: {orig_exception}')
        self.orig_exception = orig_exception

class Config:
    __home = os.environ.get('HOME')
    __xdg_config_home = os.environ.get('XDG_CONFIG_HOME')

    __config_dir = (
            os.path.join(__home, '.config/pastemngr')
            if __xdg_config_home == None
            else os.path.join(__xdg_config_home, 'pastemngr')
    )

    @classmethod
    def create_config_folder(self):
        try:
            os.mkdir(self.__config_dir)
        except FileExistsError:
            pass

    @classmethod
    def entry(self, name):
        return os.path.join(self.__config_dir, name)

    @classmethod
    def read_dev_key(self):
        try:
            file_ref = open(self.entry('dev_key'), 'r')
        except FileNotFoundError as e:
            raise DevKeyNotFoundError('dev_key file not found, please create it and provide a developer key.', e)

        dev_key = file_ref.readline().rstrip('\r\n')
        file_ref.close()

        return dev_key

    @classmethod
    def write_dev_key(self, dev_key):
        with open(self.entry('dev_key'), 'w') as f:
            f.write(dev_key)



