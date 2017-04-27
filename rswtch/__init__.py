import conf
import firmata

# factory function
def init(conf_file):
    conf_file = conf.read_file(conf_file)

    eligible_all_sections = []
    eligible_firmata_channels = []

    all_sections = conf_file.sections()

    ##### parse config file #####
    for s in all_sections:
        conf_firmata = firmata.parse(conf_file, s)

        # if required firmata conf is OK, call the generic conf
        if conf_firmata:
            # merge dicts
            conf_generic = conf.parse(conf_file, s)
            conf_firmata.update(conf_generic)

            eligible_firmata_channels.append(conf_firmata)

    ##### initialize all channels #####
    channels = []
    for c in eligible_firmata_channels:
        ch = firmata.init_channel(c)
    
        if ch:
            channels.append(ch)

    for ch in channels:
        ch.down()

    return tuple(channels)
