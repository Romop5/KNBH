#!/usr/bin/env python3.6


import finder
import sys
import re
import signal
import const


class Dormitory():

    def __init__(self, argv):
        self.__block = None
        self.__floor = None

        for arg in argv[1:]:
            if re.match('^--block=.+$', arg):
                self.__block = check_block(arg[8:])
            elif re.match('^--floor=.+$', arg):
                self.__floor = check_floor(arg[8:])
            else:
                error('Wrong arguments!\n', 1)

    def block(self):
        return self.__block

    def floor(self):
        return self.__floor

    def rooms(self):
        a = self.__floor * 100
        b = (a + 100) - 1
        return range(a, b+1)


def print_help():
    sys.stdout.write(const.HELP)


def signal_handler(signal, frame):
    sys.stdout.write("\n")
    sys.exit(0)


def error(message, exitcode):
    sys.stderr.write(message)
    sys.exit(exitcode)


def check_block(string):
    if re.match('^(B0[2457]|A0[2-5]|C0[1-3])$', string, re.IGNORECASE):
        return string.lower()
    else:
        error(string+'\nWrong block!\n', 3)


def check_floor(string):
    try:
        number = int(string)
    except ValueError:
        error(string+'\nWrong floor number!\n', 2)
    if number >= 0:
        return int(string)
    else:
        error(string+'\nWrong floor number!\n', 2)


def print_header(color, block, floor):
    colres = const.COLOR_RESET
    string = ''

    string += '======='
    string += '%s%s%s -' % (color, block, colres)
    string += ' %s%s floor%s' % (color, str(floor), colres)
    string += '======='

    print(string)


def print_footer():
    print("===========================")


def print_person(number, person):
    string = ''

    string += ' %s%s%s ' % (const.COLOR_REGULAR_GREEN, str(number), const.COLOR_RESET)

    if person.isWoman():
        string += '%s%s%s' % (const.COLOR_BOLD_RED, person.getName(), const.COLOR_RESET)
    else:
        string += '%s' % (person.getName())

    print(string)


def init():

    if len(sys.argv) == 1:
    	error('Wrong arguments!\n', 1)

    elif len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print_help()
        sys.exit(0)

    elif len(sys.argv) != 3:
    	error('Wrong arguments!\n', 1)

    D = Dormitory(sys.argv)

    print_header(const.COLOR_BOLD_GREEN, D.block().upper(), D.floor())

    for number in D.rooms():
        names = finder.get(D.block(), number)
        if names != None:
            for person in names:
                print_person(number, person)

    print_footer()


###############################################################################


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    init()
