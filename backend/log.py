"""
Wrappers around the built-in print() method that splits printing into different logging levels
"""

# levels can be activated and deactivated independently so that only certain messages are logged
levels = {
    'error': True,
    'warn': True,
    'info': True,
    'debug': False
}


def error(s):
    """log an error (something is broken!)"""
    if levels['error']:
        print(s)


def warn(s):
    """log a warning (something not-so-great happened, but nothing broke)"""
    if levels['warn']:
        print(s)


def info(s):
    """log a status (most basic print method)"""
    if levels['info']:
        print(s)


def debug(s):
    """log some debugging info (used for debugging)"""
    if levels['debug']:
        print(s)
