import ConfigParser
from pyfirmata import Arduino, serial, pyfirmata 

from channel import Channel


class GpioFirmata(Channel):
    port = {}

    def __init__(self, conf):
        port = conf['port']
        mode = conf['mode']
        inverted_logic = conf['inverted_logic']

        super(self.__class__, self).__init__(conf)
    
        if not port in GpioFirmata.port:
            GpioFirmata.port[port] = Arduino(port)
    
        self.__pin = GpioFirmata.port[port].get_pin(mode)
    
        if inverted_logic:
            self.__up = 0
            self.__down = 1
        else:
            self.__up = 1
            self.__down = 0

    def up(self):
        self.__pin.write(self.__up)
    
    def down(self):
        self.__pin.write(self.__down)
    
    def reset(self):
        self.__pin.write(self.__down)
        sleep(2)
        self.__pin.write(self.__up)
    
    def toggle(self):
        if self.__pin.read() == self.__up:
            self.__pin.write(self.__down)
    	else:
    	    self.__pin.write(self.__up)
    
    def status(self):
        s = self.__pin.read()
        return 'up' if s==self.__up else 'down'


def parse(conf_file, section):
    d = {}

    # check if it's really a firmata channel
    try:
        conf_type = conf_file.get(section, 'type')
    except ConfigParser.NoOptionError:
        return None

    ##### check required options #####
    if (conf_file.has_option(section, 'port') and
            conf_file.has_option(section, 'mode')):
        d['port'] = conf_file.get(section, 'port')
        d['mode'] = conf_file.get(section, 'mode')
    else:
        return None

    ##### check optional options #####
    # inverted logic
    try:
        il = conf_file.getboolean(section, 'inverted_logic')
    except ConfigParser.NoOptionError:
        il = False
    d['inverted_logic'] = il

    return d

def init_channel(conf):
    c = None
    try:
        c = GpioFirmata(conf)
    except serial.serialutil.SerialException:
        print("warning: could not open port {0} for channel {1},"
                " skipping".format(conf['port'], conf['channel']))
    except pyfirmata.PinAlreadyTakenError:
        print("warning: channel pin '{0}' on port {1} already taken"
                .format(conf['mode'], conf['port']))
    except (IOError, IndexError):
        print("warning: possible wrong channel mode description")

    return c
