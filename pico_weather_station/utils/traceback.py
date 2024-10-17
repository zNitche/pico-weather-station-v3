# https://github.com/micropython/micropython-lib/blob/master/python-stdlib/traceback/traceback.py

import sys


def print_exception(e: Exception):
    sys.print_exception(e)


def format_exc():
    return "".join(repr(*sys.exc_info()))
