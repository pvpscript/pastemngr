import os

class Config:
    __home = os.getenv('HOME')
    __xdg_config_home = os.getenv('XDG_CONFIG_HOME')

    __config_dir = self.__home + '/.config/tpastebin/' \
            if __xdg_config_home == None \
            else __xdg_config_home + '/tpastebin/'

    @classmethod
    def entry(self, name):
        return self.__config_dir + name 

    @classmethod
    def read_dev_key(self):
        file_ref = open(self.entry('dev_key'), 'r')

        dev_key = file_ref.readline().rstrip('\r\n')
        file_ref.close()

        return dev_key
