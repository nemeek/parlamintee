#!/usr/bin/env python3
"""
Read json file
"""
import argparse
import itertools

import ijson

def iter_items(parser):
    for prefix, event, value in parser:
        #yield prefix, event, value
        #if event in ['string','null','number']:
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
    with open(args.infile, 'rb') as infile:
        parser = ijson.parse(infile)
        #for key, value in ijson.kvitems(infile, '.item'):
        #    print('key: {}, value: {}'.format(key, value))
        # for parent, data_type, value in parser:
            #if parent == 'item':
            # print ('parent={}, data type={}, value={}'.format(parent, data_type, value))
        items = [x for x in iter_items(parser)] # if x[0] == 'item.kuupaev']
        #print(len(items))
        for p, k, v in items:
            print('{} --- {} --- {}'.format(p, k, limit(v)))
        #print(dict(itertools.islice(items, 10)))
        #asjad = ijson.items(infile,'.items')
        #asjaolud = (o for o in asjad)
        #kpd = [k for k, v in asjad if k=='esineja']
        #print(len(list(asjaolud)))



if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)