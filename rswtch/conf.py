import ConfigParser

def find_file(self):
    home_conf = os.path.join(os.environ['HOME'], '.rswtch.conf')
    etc_conf = os.path.join('etc', 'rswtch.conf')

    if os.path.isfile(home_conf):
        return(home_conf)
    elif os.path.isfile(etc_conf):
        return(etc_conf)

def read_file(conf_file):
    if not conf_file:
        conf_file = find_file()

        if not conf_file:
            print('error: no config file found')
            exit(1)

    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf

def parse(conf_file, section):
    conf = {}
    conf['channel'] = section

    return conf
