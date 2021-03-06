import sys


def info(msg: str) -> None:
    '''Log a message to stderr.'''
    print(f'[\033[0;32m*\033[0m] {msg}', file=sys.stderr)


def warn(msg: str) -> None:
    '''Log a warning to stderr.'''
    print(f'[\033[0;33m*\033[0m] {msg}', file=sys.stderr)


def die(msg: str) -> None:
    '''Log an error to stderr and exit.'''
    print(f'[\033[0;31m*\033[0m] {msg}', file=sys.stderr)
    sys.exit(1)
