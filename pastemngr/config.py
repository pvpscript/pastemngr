import os

class Config:
    __home = os.getenv('HOME')
    __xdg_config_home = os.getenv('XDG_CONFIG_HOME')

    __config_dir = self.__home + '/.config/pastemngr/' \
            if __xdg_config_home == None \
            else __xdg_config_home + '/pastemngr/'

    @classmethod
    def entry(self, name):
        return self.__config_dir + name 

    @classmethod
    def read_dev_key(self):
        try:
            file_ref = open(self.entry('dev_key'), 'r')
        except FileNotFoundError:
            raise FileNotFoundError('dev_key file not found, please create it and provide a developer key.')

        dev_key = file_ref.readline().rstrip('\r\n')
        file_ref.close()

        return dev_key

    @classmethod
    def write_dev_key(self, dev_key):
        with open(self.entry('dev_key'), 'w') as f:
            f.write(dev_key)



