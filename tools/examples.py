#!/usr/bin/env python3
"""
Find tei examples

Usage:
./examples.py ~/GIT/github/ParlaMint/Data/


"""
import argparse
# import itertools
from os import listdir
from os.path import isdir, isfile, join

# import ijson

## --- Classes ---

class PMDir(str):
    def __init__(self, dn):
        self.dn = dn
        self.country = self.dn.split('-', 1)[-1]

    # def __repr__(self):
    #     return self.dn

class Filles:
    def __init__(self, path, stw = 'ParlaMint'):
        self.path = path
        self.stw = stw
        self.dirs = [PMDir(f) for f in listdir(self.path) if isdir(join(self.path, f)) and f.startswith(self.stw)]
        self.dns = None
        self.fltr = 'all'
        # self.files = [listdir(join(path, x)) for x in self.dirs]
    def dirnames(self, filter: str = 'all'):
        self.fltr = filter
        if filter == 'all':
            self.dns = self.dirs
        else:
            self.dns = [x for x in self.dirs if filter in x]
        return self.dns

    def content(self):
        self.files = [[f for f in listdir(join(self.path,x))] for x in self.dns]
        return self.files
## --- Functions ---

def show(what: str, dirs: list, path: str):
    """
    Näitab kausta sisu
    :param what:
    :return: None
    """
    if what == 'all':
        pass


def files(inpath, stw):
    onlydirs = [f for f in listdir(inpath) if isdir(join(inpath, f)) and f.startswith(stw)]
    subdirs = [listdir(join(inpath,x)) for x in onlydirs]
    for i in subdirs:
        yield i

def returnparser():
    parser = argparse.ArgumentParser(
        description='find TEI examples'
    )
    parser.add_argument('inpath')
    parser.add_argument('-s', '--show', default='all')
    parser.add_argument('-l', '--list', action='store_true', default=False)
    return parser

def limit(text):
    try:
        if len(text) > 30:
            return text[:29] + '...'
    except TypeError:
        return text
    return text


def main(p: argparse.ArgumentParser):
    args = p.parse_args()
    if args.show:
        print ('It\'s showtime!')

    if args.inpath:
        f = Filles(path = args.inpath)
        f.dirnames(args.show)
        print(f.content())


if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)