#!/usr/bin/env python3.6


import finder
import sys
import re
import signal
import const
import os


class Dormitory():

    def __init__(self, argv):
        self.__block = None
        self.__floor = None
        self.__ping = False
        self.__room = None

        for arg in argv[1:]:
            if re.match('^--block=.+$', arg):
                self.__block = check_block(arg[8:])
            elif re.match('^-b=.+$', arg):
                self.__block = check_block(arg[3:])
            elif re.match('^--floor=.+$', arg):
                self.__floor = check_number(arg[8:])
            elif re.match('^-f=.+$', arg):
                self.__floor = check_number(arg[3:])
            elif re.match('^--ping$', arg) or re.match('^-p$', arg):
                self.__ping = True
            elif re.match('^--room=.+$', arg):
                self.__room = check_number(arg[7:])
            elif re.match('^-r=.+$', arg):
                self.__room = check_number(arg[3:])
                self.__floor = room_to_floor(self.__room)
            elif arg == '-h' or arg == '--help':
                print_help()
                exit(0)
            else:
                error('Wrong arguments!\n', 1)

    def block(self):
        return self.__block

    def floor(self):
        return self.__floor

    def ping(self):
        return self.__ping

    def rooms(self):
        if self.__room != None:
            return range(self.__room, self.__room + 1)
        a = self.__floor * 100
        b = (a + 100) - 1
        return range(a, b + 1)


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


def check_number(string):
    try:
        number = int(string)
    except ValueError:
        error(string+'\nWrong number!\n', 2)
    if number >= 0:
        return number
    else:
        error(string+'\nWrong number!\n', 2)


def room_to_floor(number):
    room = str(number)
    if len(room) == 3:
        return room[:1]
    else:
        return room[:2]


def print_header(color, block, floor):
    colres = const.COLOR_RESET
    string = ''

    string += '\t\t['
    string += '%s%s%s -' % (color, block, colres)
    string += ' %s%s floor%s' % (color, str(floor), colres)
    string += ']'

    print(string)


def print_footer():
    print(" ---------------------------------")


def print_footer_ping():
    print(" --------------------------------- -------------")


def get_person(number, person):
    string = ''

    string += '| %s%s%s | ' % (const.COLOR_REGULAR_GREEN,
                               str(number), const.COLOR_RESET)

    rem = 30 + 13
    if person.isWoman():
        string += '%s%s%s' % (const.COLOR_BOLD_RED,
                              person.getName(), const.COLOR_RESET)
        rem += 13
    else:
        string += '%s' % (person.getName())

    rem = rem - len(string)
    string += rem * " "
    string += "|"
    return string


def ping(host):
    response = os.system("ping -c 1 -w1 " + host + " > /dev/null 2>&1")
    return response == 0


def init():

    if len(sys.argv) == 1:
        error('Wrong arguments!\n', 1)

    elif len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print_help()
        sys.exit(0)

    elif len(sys.argv) > 6:
        error('Wrong arguments!\n', 1)

    D = Dormitory(sys.argv)

    print_header(const.COLOR_BOLD_GREEN, D.block().upper(), D.floor())

    empty_rooms = 0
    no_rooms = True
    for number in D.rooms():
        names = finder.get(D.block(), number)
        if names == None:
            # the could be no room numbers in middle of the floor
            # skip them
            if int(str(number)[-2:]) < 20:
                continue

            if empty_rooms > 0:
                # two empty rooms, stop
                # probably there are no other rooms
                break

            # maybe just empty room
            empty_rooms = empty_rooms + 1
            continue
        else:
            # reset empty rooms counter
            if empty_rooms > 0:
                empty_rooms = 0

        no_rooms = False
        if D.ping():
            status = "offline"

            online = 0
            room = str(number)
            if len(room) == 3 and (D.block().startswith("a") or D.block().startswith("d")):
                room = "0" + room

            for c in ["a", "b", "c"]:
                domain = str(D.block()) + "-" + room + c + ".kn.vutbr.cz"
                if ping(domain) or ping("w" + domain):
                    online = online + 1

            all_online = len(names) == online
            all_offline = online == 0

            print_footer_ping()
        else:
            print_footer()

        for person in names:
            if D.ping():
                print(get_person(number, person), end="")
                maybe = "?" if not all_online and not all_offline else ""
                if online > 0:
                    print("   " + const.COLOR_BOLD_BLUE + "online" +
                          maybe + const.COLOR_RESET + "\t|")
                    online = online - 1
                else:
                    print("   " + const.COLOR_REGULAR_YELLOW +
                          "offline" + maybe + const.COLOR_RESET + "\t|")

            else:
                print(get_person(number, person))

    if not no_rooms:
        if D.ping():
            print_footer_ping()
        else:
            print_footer()


###############################################################################


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    init()
