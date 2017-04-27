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

import argparse
import cmd
import shlex
import signal

from time import sleep

import rswtch


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
        print("{0:<16} {1}".format("COMMAND", "DESCRIPTION"))
        print("{0:<16} {1}".format("annotate n \"c\"",
            "annotate c in channel n (use quotes)"))
        print("{0:<16} {1}".format("down n", "turn off the n channel"))
        print("{0:<16} {1}".format("help", "this help"))
        print("{0:<16} {1}".format("quit",
            "quit rswtch"))
        print("{0:<16} {1}".format("reset n",
            "turn the n channel off and on again after 2 seconds"))
        print("{0:<16} {1}".format("status",
            "display the status of all channels,"
            "including annotations"))
        print("{0:<16} {1}".format("toggle n",
            "turn the n channel off if its on, and vice-versa"))
        print("{0:<16} {1}".format("up n", "turn on the n channel"))

    ### commands
    # up
    def do_up(self, line):
        parser = shlex.shlex(line)

        try:
            c = int(parser.get_token())
            ch[c].up()
        except (IndexError, ValueError):
            print("no channel")

    # down
    def do_down(self, line):
        parser = shlex.shlex(line)

        try:
            c = int(parser.get_token())
            ch[c].down()
        except (IndexError, ValueError):
            print("no channel")

    # toggle
    def do_toggle(self, line):
        parser = shlex.shlex(line)

        try:
            c = int(parser.get_token())
            ch[c].toggle()
        except (IndexError, ValueError):
            print("no channel")

    # reset
    def do_reset(self, line):
        parser = shlex.shlex(line)

        try:
            c = int(parser.get_token())
            ch[c].reset()
        except (IndexError, ValueError):
            print("no channel")

    # status
    def do_status(self, line):
        print("{0:>2} {1:<24.24} {2:<6} {3:<24.24}"
                .format("CH", "CHANNEL", "STATUS", "ANNOTATION"))

        for c in enumerate(ch):
            print("{0:>2} {1:<24.24} {2:<6} {3:<24.24}"
                    .format(c[0], c[1].channel, c[1].status(),
                        c[1].annotation))

    # annotate
    def do_annotate(self, line):
        parser = shlex.shlex(line, posix=True)

        try:
            c = int(parser.get_token())
            ch[c].annotation = parser.get_token()
        except (IndexError, ValueError):
            print("no channel")

    # quit
    def do_quit(self, line):
        exit(0)

    # handle ^C
    @staticmethod
    def handle_sigint(signum, frame):
        exit(0)


if __name__ == '__main__':
    opts = argparse.ArgumentParser()
    opts.add_argument("-f", help="specify config file")
    args = opts.parse_args()

    ch = rswtch.init(args.f)

    # start shell
    signal.signal(signal.SIGINT, Sh.handle_sigint)
    Sh().cmdloop()
