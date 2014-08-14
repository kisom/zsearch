#!/usr/bin/env python
"""
zsearch is a utility for searching zlib-compressed files for a
search string. It was really designed for use with the Git object
store, i.e. to aid in the recovery of files after Git does what Git
do.
"""

import argparse
import os
import os.path
import re
import zlib


def search_file(path, search):
    """
    search_file opens the file, decompresses it, and searches for
    the expression in the file. If found, it prints the path and the
    decompressed contents.
    """

    data = open(path).read()

    try:
        zdata = zlib.decompress(data)
    except zlib.error:
        pass
    except Exception:
        return
    else:
        data = zdata
    if re.search(search, data):
        print '%s:\n%s\n' % (path, data)


def search_dir(path, search):
    """
    walk a directory, searching each file found for the search term.
    """

    for root, _, files in os.walk(path):
        for name in files:
            search_file(os.path.join(root, name), search)


def search_files(paths, search):
    """
    Walk through a list of paths, running search_dir or search_file as
    appropriate.
    """

    for path in paths:
        print path
        if os.path.isfile(path):
            search_file(path, search)
        else:
            search_dir(path, search)


def show_files(paths):
    """Print the zlib-compress list of files passed in."""
    for name in paths:
        if os.path.isfile(name):
            print '%s:\n%s\n' % (name, zlib.decompress(open(name).read()))
        else:
            for root, _, files in os.walk(name):
                for name in files:
                    name = os.path.join(root, name)
                    zdata = zlib.decompress(open(name).read())
                    print '%s:\n%s\n' % (name, zdata)


def main():
    """
    main contains the argument parser and determines whether to
    actually search or just print files to stdout.
    """

    parser = argparse.ArgumentParser(description='Search zlib-compressed ' +
                                     'files (e.g. the git object store)')
    parser.add_argument('-s', '--search', action='store',
                        help='search expression (should be a perl-' +
                        'compatible regular expression)')
    parser.add_argument('paths', nargs='?', default='.git/objects',
                        help='list of paths to search')
    args = parser.parse_args()

    if args.search:
        search_files(args.paths, args.search)
    else:
        show_files(args.paths)


if __name__ == "__main__":
    main()
