#!/usr/bin/env python2.7
#
# Copyright (c) 2016, Daniel Bolgheroni.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# TODO:
# . include README.md documentation
# . include sample for rswtch.conf
# . improve readability of commands in Sh

import argparse
import cmd
import signal
import shlex
from time import sleep

from pyfirmata import Arduino, serial

from conf import Config


class Sh(cmd.Cmd):
    prompt = 'rswtch> '
    intro = 'type \'help\' to see available commands'

    def default(self, line):
        print(line + ": not found")

    def do_EOF(self, line):
        exit(0)

    # overwrite help, since commands are simple, do not need independent
    # help for each command
    def do_help(self, line):
        print('down n: where n is the channel number from 1 to 4')
        print('up n: where n is the channel number from 1 to 4')
        print('reset n: where n is the channel number from 1 to 4')
        print('status: shows the status of all channels')
        print('help: this help')

    ### commands
    # up
    def do_up(self, line):
        parser = shlex.shlex(line)
        c = parser.get_token()

        try:
            channels[c].up()
        except KeyError:
            print("no channel")

    # down
    def do_down(self, line):
        parser = shlex.shlex(line)
        c = parser.get_token()

        try:
            channels[c].down()
        except KeyError:
            print("no channel")

    # reset
    def do_reset(self, line):
        parser = shlex.shlex(line)
        c = parser.get_token()

        try:
            channels[c].reset()
        except KeyError:
            print("no channel")

    # status
    def do_status(self, line):
        status()

    def do_annotate(self, line):
        parser = shlex.shlex(line, posix=True)
        c = parser.get_token()

        try:
            channels[c].annotation = parser.get_token()
        except KeyError:
            print("no channel")

    # quit
    def do_quit(self, line):
        exit(0)

    # handle ^C
    @staticmethod
    def handle_sigint(signum, frame):
        exit(0)


class Channel():
    # the relay module uses inverted logic, so
    # 1 to bring pin down and 0 bring pin up
    def __init__(self, pin, boardname):
        self.__pin = pin
        self.boardname = boardname
        self.annotation = None

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
    print("{0:>2} {1:<6} {2:<20.20} {3:<40.40}"
            .format("CH", "STATUS", "BOARD", "ANNOTATION"))
    print("{0:>2} {1:<6} {2:<20.20} {3:<40.40}"
            .format("1", ch1.status, ch1.boardname, ch1.annotation))
    print("{0:>2} {1:<6} {2:<20.20} {3:<40.40}"
            .format("2", ch2.status, ch2.boardname, ch2.annotation))
    print("{0:>2} {1:<6} {2:<20.20} {3:<40.40}"
            .format("3", ch3.status, ch3.boardname, ch3.annotation))
    print("{0:>2} {1:<6} {2:<20.20} {3:<40.40}"
            .format("4", ch4.status, ch4.boardname, ch4.annotation))

if __name__ == '__main__':
    opts = argparse.ArgumentParser()
    opts.add_argument("-v", action="store_true",
            help="shows board Firmata firmware version")
    opts.add_argument("-f",
            help="specify config file")
    opts.add_argument("dev", help="serial device")
    args = opts.parse_args()

    # init Firmata module
    try:
        board = Arduino(args.dev)
    except serial.serialutil.SerialException:
        print("could not open port {0}".format(args.dev))
        exit(1)

    # try to get board firmata version
    # this fails most of the times
    if args.v:
        v = board.get_firmata_version()
        try:
            print("{0}.{1}".format(v[0], v[1]))
            exit(0)
        except (NameError, TypeError):
            print("could not get board firmata version")
            exit(1)

    # handle configuration file
    if args.f:
	config = Config(args.f)
    else:
	config = Config()

    # turn off board led
    led = board.get_pin('d:13:o')
    led.write(0)

    # configuring pins
    ch1 = Channel(board.get_pin('d:9:o'), config.get_boardname(1))
    ch2 = Channel(board.get_pin('d:8:o'), config.get_boardname(2))
    ch3 = Channel(board.get_pin('d:7:o'), config.get_boardname(3))
    ch4 = Channel(board.get_pin('d:6:o'), config.get_boardname(4))

    channels = {'1': ch1, '2': ch2, '3': ch3, '4': ch4}

    # start shell
    signal.signal(signal.SIGINT, Sh.handle_sigint)
    Sh().cmdloop()
