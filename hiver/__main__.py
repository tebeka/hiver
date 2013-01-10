#!/usr/bin/env python

from . import connect, DEFAULT_HOST, DEFAULT_PORT, __version__
from .hive_service import ThriftHive
import re
from os import environ
from os.path import expanduser, isfile
from sys import stdin
import atexit

HOST = environ.get('HIVE_HOST', DEFAULT_HOST)
PORT = int(environ.get('HIVE_PORT', DEFAULT_PORT))

HISTFILE = expanduser('~/.hive-history')


def fix_hql(hql):
    return hql.replace(';', '').strip()


def iterhql(getline):
    buf = ''

    while True:
        try:
            line = getline()
        except EOFError:
            break

        if not line:
            break

        buf += line
        while True:
            idx = buf.find(';')
            if idx == -1:
                break
            hql = fix_hql(buf[:idx])
            if hql:
                yield hql
            buf = buf[idx+1:]

    hql = fix_hql(buf)
    if hql:
        yield hql


def execute(client, hql):
    if not hql.strip():
        return

    try:
        client.execute(hql)
        lnum = 0
        for lnum, line in enumerate(client.fetchAll(), 1):
            print('  {}'.format(line))
        print('({} rows)\n'.format(lnum))
    except ThriftHive.HiveServerException as e:
        print('ERROR: {}'.format(e))
        return


def repl_line():
    try:
        return raw_input('[hiver] ').strip()
    except (KeyboardInterrupt, EOFError):
        return ''


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='')
    parser.add_argument('--host', default=HOST)
    parser.add_argument('--port', default=PORT, type=int)
    parser.add_argument('script', help='script file', nargs='?')
    parser.add_argument('--version', action='version',
                        version='hiver {}'.format(__version__))
    args = parser.parse_args(argv[1:])

    client = connect(args.host, args.port)

    if args.script:
        if args.script == '-':
            fo = stdin
        else:
            try:
                fo = open(args.script)
            except IOError as e:
                raise SystemExit(
                    'error: cannot open {} - {}'.format(args.script, e))
        getline = fo.readline
    else:
        import readline
        if isfile(HISTFILE):
            readline.read_history_file(HISTFILE)
        atexit.register(lambda: readline.write_history_file(HISTFILE))
        getline = repl_line

    for hql in iterhql(getline):
        execute(client, hql)


if __name__ == '__main__':
    main()
