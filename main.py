#!/usr/bin/env python3.6

import finder
import sys
import re
import signal

###############################################################################


class Colors():

    reset        = "\033[0m"

    bold_red     = "\033[1m\033[31m"
    bold_green   = "\033[1m\033[32m"
    bold_yellow  = "\033[1m\033[33m"
    bold_blue    = "\033[1m\033[34m"
    bold_magenta = "\033[1m\033[35m"
    bold_cyan    = "\033[1m\033[36m"

    regular_red     = "\033[31m"
    regular_green   = "\033[32m"
    regular_yellow  = "\033[33m"
    regular_blue    = "\033[34m"
    regular_magenta = "\033[35m"
    regular_cyan    = "\033[36m"
    regular_black   = "\033[30m"
    regular_white   = "\033[0m\033[37m"


class Rooms():

    fr=None
    to=None
    fl=None
    bl=None

    def __str__(self):
        return 'FROM:\t'+str(self.fr)+'\nTO:\t'+str(self.to)+'\nFLOOR:\t'+str(self.fl)+'\nBLOCK:\t'+self.bl

###############################################################################


def print_help():

    message= '\nScript\'s parameters:\n\n' + \
             '\t[ [-rf][-rt]|[fl] ][-bl] \n\n' + \
             '\tRooms from number A:\n' + \
             '\t[-rf=A]\n\n' + \
             '\tRooms to number B:\n' + \
             '\t[-rt=B]\n\n' + \
             '\tRooms from floor N:\n' + \
             '\t[-fl=N]\n\n' + \
             '\tRooms from block X:\n' + \
             '\t[-bl=X]\n\n' + \
             '\tHelp:\n' + \
             '\t[-h]\n\n'

    sys.stdout.write(message)


def signal_handler(signal, frame):
    sys.stdout.write("\n")
    sys.exit(0)


def error(message, exitcode):
    sys.stderr.write(message)
    print_help()
    sys.exit(exitcode)


def check_room_number(string):
    try:
        number = int(string)
    except ValueError:
        error("Wrong room number!\n", 2)
    if number >= 0:
        return int(string)
    else:
        error("Wrong room number!\n", 2)


def check_block(string):
    if re.match("^(B0[2457]|A0[2-5]|C0[1-3])$", string, re.IGNORECASE):
        return string.lower()
    else:
        error("Wrong block!\n", 3)


def load_rooms(rooms, argv):
    for arg in argv[1:]:
        if re.match('^-rf=.*$', arg) and rooms.fr == rooms.fl is None:
            rooms.fr = check_room_number(arg[4:])
        elif re.match('^-rt=.*$', arg) and rooms.to == rooms.fl is None:
            rooms.to = check_room_number(arg[4:])
        elif re.match('^-fl=.*$', arg) and rooms.fl == rooms.fr == rooms.to is None:
            rooms.fl = check_room_number(arg[4:])
        elif re.match('^-bl=.*$', arg) and rooms.bl is None:
            rooms.bl = check_block(arg[4:])
        else:
            error('Wrong arguments!\n', 1)

    if not rooms.bl:
        error('Wrong arguments!\n', 1)

    if rooms.fl:
        rooms.fr = rooms.fl * 100
        rooms.to = (rooms.fr + 100) - 1
    elif rooms.fr > rooms.to:
        rooms.fr, rooms.to = rooms.to, rooms.fr


def init():

    if len(sys.argv) == 2 and sys.argv[1] == '-h': print_help(); sys.exit(0)

    C = Colors()
    R = Rooms()

    load_rooms(R, sys.argv)

    print("=======", C.bold_green+R.bl.upper()+C.reset, "=======")
    for room_number in range(R.fr, R.to+1):
        names = finder.get(R.bl, room_number)
        if names != None:
            for person in names:
                print(" "+C.regular_green+str(room_number)+C.reset, end=" ")
                if person.isWoman():
                    print(C.bold_red, end="")
                else:
                    print(C.regular_white, end="")
                print(person.getName(), C.reset)
    print("===================")

    sys.exit(0)

###############################################################################


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    init()
