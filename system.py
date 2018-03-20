import sys


def signal_handler(signal, frame):
    sys.stdout.write("\n")
    sys.exit(0)


def error(message, exitcode):
    sys.stderr.write(message)
    sys.exit(exitcode)
