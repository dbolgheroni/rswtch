#!/usr/bin/env python2.7
#
# control a 3 channel rswtch
#
# IMPORTANT: the relay module uses inverted logic
# . 1 to put pin down
# . 0 to put pin up

import argparse
from time import sleep

from pyfirmata import Arduino, util, serial
from pyfirmata import Board

def reset(ch):
    ch.write(1)
    sleep(2)
    ch.write(0)

def up(ch):
    ch.write(0)

def down(ch):
    ch.write(1)

def get_status(ch1, ch2, ch3):
    status = []
    status.append(ch1.read())
    status.append(ch2.read())
    status.append(ch3.read())

    return status

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

    # turn off board led
    led = board.get_pin('d:13:o')
    led.write(0)

    # configuring pins
    ch1 = board.get_pin('d:9:o')
    ch2 = board.get_pin('d:8:o')
    ch3 = board.get_pin('d:7:o')

    # initialize all channels
    ch1.write(0)
    ch2.write(0)
    ch3.write(0)

    prompt = "> "
    while 1:
        cmd = raw_input(prompt)

        if cmd == 'r1':
            reset(ch1)
        elif cmd == 'r2':
            reset(ch2)
        elif cmd == 'r3':
            reset(ch3)
        elif cmd == 'u1':
            up(ch1)
        elif cmd == 'u2':
            up(ch2)
        elif cmd == 'u3':
            up(ch3)
        elif cmd == 'd1':
            down(ch1)
        elif cmd == 'd2':
            down(ch2)
        elif cmd == 'd3':
            down(ch3)
        elif cmd == 's':
            s = get_status(ch1, ch2, ch3)
            for i in [0, 1, 2]:
                print("ch{0}: {1}".
                        format(i+1, 'up' if s[i] == 0 else 'down'))
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
