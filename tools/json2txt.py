#!/usr/bin/env python3
"""
Read json file
"""
import argparse
import os.path

import ijson

UTTERANCE_Y = 'U'

def iter_items(parser):
    for prefix, event, value in parser:
        if prefix:
            yield prefix, event, value
        else:
            yield '======', '======', '======'


def returnparser():
    parser = argparse.ArgumentParser(
        description='Read json file'
    )
    parser.add_argument('infile')
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
    filenamestem = os.path.splitext(os.path.basename(args.infile))[0]
    with open(args.infile, 'rb') as infile:
        parser = ijson.parse(infile)
        items = [x for x in iter_items(parser)] # if x[0] == 'item.kuupaev']
        work = False
        utrno = 0
        utid = ''
        for p, k, v in items:
            if k == 'map_key' and v == 'speech':
                work = True
            if k == 'end_array':
                work = False
            if work and k == 'string':
                utrno +=1
                utid = '{}_{}{}'.format(filenamestem, UTTERANCE_Y, utrno)
                print ('{}\t{}'.format(utid, v))


if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)