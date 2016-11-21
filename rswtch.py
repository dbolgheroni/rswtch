#!/usr/bin/env python2.7

import argparse
from time import sleep

from pyfirmata import Arduino, serial

from conf import Config


class Channel():
    # the relay module uses inverted logic, so
    # 1 to bring pin down and 0 bring pin up
    def __init__(self, pin, boardname):
        self.__pin = pin
        self.boardname = boardname

        # up by default
        self.__pin.write(0)

    def up(self):
        self.__pin.write(0)

    def down(self):
        self.__pin.write(1)

    def reset(self):
        self.__pin.write(1)
        sleep(2)
        self.__pin.write(0)

    @property
    def status(self):
        return 'up' if self.__pin.read() == 0 else 'down'

def status():
    print("channel1: {0} ({1})".format(ch1.status, ch1.boardname))
    print("channel2: {0} ({1})".format(ch2.status, ch2.boardname))
    print("channel3: {0} ({1})".format(ch3.status, ch3.boardname))
    print("channel4: {0} ({1})".format(ch4.status, ch4.boardname))

if __name__ == '__main__':
    opts = argparse.ArgumentParser()
    opts.add_argument("dev", help="serial device")
    args = opts.parse_args()

    # intro
    print("rswtch, type 'h' to see the available commands")
    print("initializing firmata library")
    try:
        board = Arduino(args.dev)
    except serial.serialutil.SerialException:
        print("could not open port {0}".format(args.dev))
        exit(1)

    # try to get board firmata version
    # this fails most of the times
    v = board.get_firmata_version()
    try:
        print("board firmata version: {0}.{1}".format(v[0], v[1]))
    except (NameError, TypeError):
        print("could not get board firmata version")

    # handle configuration file
    config = Config()

    # turn off board led
    led = board.get_pin('d:13:o')
    led.write(0)

    # configuring pins
    ch1 = Channel(board.get_pin('d:9:o'), config.get_boardname(1))
    ch2 = Channel(board.get_pin('d:8:o'), config.get_boardname(2))
    ch3 = Channel(board.get_pin('d:7:o'), config.get_boardname(3))
    ch4 = Channel(board.get_pin('d:6:o'), config.get_boardname(4))

    prompt = "> "
    while 1:
        cmd = raw_input(prompt)

        if cmd == 'r1':
            ch1.reset()
        elif cmd == 'r2':
            ch2.reset()
        elif cmd == 'r3':
            ch3.reset()
        elif cmd == 'r4':
            ch4.reset()
        elif cmd == 'u1':
            ch1.up()
        elif cmd == 'u2':
            ch2.up()
        elif cmd == 'u3':
            ch3.up()
        elif cmd == 'u4':
            ch4.up()
        elif cmd == 'd1':
            ch1.down()
        elif cmd == 'd2':
            ch2.down()
        elif cmd == 'd3':
            ch3.down()
        elif cmd == 'd4':
            ch4.down()
        elif cmd == 's':
            status()
        elif cmd == 'h':
            print("d{ch}: down channel, e.g. d1 to put channel 1 down")
            print("u{ch}: up channel, e.g. u1 to put channel 1 up")
            print("r{ch}: reset channel, e.g. r1 to reset channel 1")
            print("s: status of all channels")
            print("h: this help")
            print("q: quit")
        elif cmd == 'q':
            exit(0)
        else:
            print('invalid command')
