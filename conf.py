import os
import ConfigParser


class Config():
    def __init__(self, *conf_file):
        self.__config = ConfigParser.ConfigParser()

        if len(conf_file) == 0:
            self.__config.read(self.find_conf_file())
        else:
            self.__config.read(conf_file[0])

    @staticmethod
    def find_conf_file():
        home_conf = os.path.join(os.environ['HOME'], '.rswtch.conf')
        etc_conf = os.path.join('etc', 'rswtch.conf')

        if os.path.isfile(home_conf):
            return(home_conf)
        elif os.path.isfile(etc_conf):
            return(etc_conf)

    def get_boardname(self, ch):
        try:
            return(self.__config.get('channel' + str(ch), 'board'))
        except ConfigParser.NoSectionError:
            return('unknown board')
        except ConfigParser.NoOptionError:
            return('unknown board')
