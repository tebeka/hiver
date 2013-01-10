#!/usr/bin/env python

from . import connect, DEFAULT_HOST, DEFAULT_PORT, __version__
from .hive_service import ThriftHive
import re
from os import environ
from os.path import expanduser, isfile

HOST = environ.get('HIVE_HOST', DEFAULT_HOST)
PORT = int(environ.get('HIVE_PORT', DEFAULT_PORT))

HISTFILE = expanduser('~/.hive-history')


def fix_hql(hql):
    # 'SHOW TABLES;' -> 'SHOW TABLES'
    return re.sub('\s*;+\s*$', '', hql, re.M|re.S)


def repl(client):
    import readline
    if isfile(HISTFILE):
        readline.read_history_file(HISTFILE)

    while True:
        try:
            hql = raw_input('[hive] ').strip()
        except (KeyboardInterrupt, EOFError):
            readline.write_history_file(HISTFILE)
            return

        hql = fix_hql(hql)
        try:
            client.execute(hql)
            for line in client.fetchAll():
                print(line)
        except ThriftHive.HiveServerException as e:
            print('ERROR: {}'.format(e))


def script(client, filename):
    with open(filename) as fo:
        hql = fo.read()

    hql = fix_hql(hql)

    if hql.endswith(';'):
        hql = hql[:-1]

    client.execute(hql)
    for line in client.fetchAll():
        print(line)


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='')
    parser.add_argument('--host', default=HOST)
    parser.add_argument('--port', default=PORT, type=int)
    parser.add_argument('script', help='script file', nargs='?')
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args(argv[1:])

    client = connect(args.host, args.port)

    if args.script:
        script(client, args.script)
    else:
        repl(client)

if __name__ == '__main__':
    main()
