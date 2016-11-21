import os
import ConfigParser


class Config():
    def __init__(self):
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(self.find_conf_file())

    @staticmethod
    def find_conf_file():
        home_conf = os.path.join(os.environ['HOME'], '.rswtch.conf')
        etc_conf = os.path.join('etc', 'rswtch.conf')
        local_conf = 'rswtch.conf'

        if os.path.isfile(home_conf):
            return(home_conf)
        elif os.path.isfile(etc_conf):
            return(etc_conf)
        elif os.path.isfile(local_conf):
            return(local_conf)

    def get_boardname(self, ch):
        try:
            return(self.__config.get('channel' + str(ch), 'board'))
        except ConfigParser.NoSectionError:
            return('unknown board')
        except ConfigParser.NoOptionError:
            return('unknown board')
