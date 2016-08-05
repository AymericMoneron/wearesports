import argparse
import datetime
import os

def env(*args):
    # Returns the first environment variable set.
    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value
    return ''


def valid_date(d):
    try:
        return datetime.datetime.strptime(d, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(d)
        raise argparse.ArgumentTypeError(msg)
