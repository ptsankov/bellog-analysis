#!/usr/bin/python
import sys

DEBUG = True

TRUE = 't'
ERROR = 'e'
FALSE = 'f'

XSB_PATH = '/home/ptsankov/apps/XSB/bin/xsb'

COUNT = 0

def freshPredicate():
    global COUNT
    COUNT += 1
    return 'tmp' + str(COUNT)

# Log a message if set in DEBUG mode
def log(*msgs):
    if DEBUG:
        for msg in msgs:
            sys.stdout.write(str(msg))
            sys.stdout.write(' ')
        sys.stdout.write('\n')