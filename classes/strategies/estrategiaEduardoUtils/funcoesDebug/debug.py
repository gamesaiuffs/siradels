import time

DEBUG = True
DEBUG_TIME = False

def debugTime():
    if DEBUG_TIME:
        time.sleep(5)


def debug(message: str):
    if (DEBUG):
        print(message)