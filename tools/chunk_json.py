#!/usr/bin/env python3
"""
Read json file, write chunks of json file according to params
"""
import argparse
import ijson
import json
import re

import datetime
from datetime import datetime as dt

ISOFMT='%Y-%m-%d %H:%M:%S'
ISOSHORT='%Y-%m-%d'
NUMBERKEYS = ['jrk', 'haaled']
DATEPATTERN = re.compile(r'(?P<fd>[12][09][0129]\d[-][01]\d[-][0-3]\d(?P<ft> [0-2]\d:[0-5]\d:[0-5]\d)?)(?: - (?P<sd>[12][09][0129]\d[-][01]\d[-][0-3]\d(?P<st> [0-2]\d:[0-5]\d:[0-5]\d)?))?')
NUMBERPATTERN = re.compile(r'(\d{1,4})(?: ?- ?(\d{1,4}))?')


def parseNumList(text: str):
    m = NUMBERPATTERN.match(text)
    if not m:
        raise argparse.ArgumentTypeError('"{}" pole number ega vahemik!'.format(text))
    else:
        start = m.group(1)
        end = m.group(2) or start
        r = [int(start), int(end)]
    return {'value_type': type(r[0]), 'min_value': min(r), 'max_value':max(r)}


def parseDates(text: str):
    m = DATEPATTERN.match(text)
    if not m:
        raise argparse.ArgumentTypeError('"{}" pole kuupäev!'.format(text))
    else:
        startf = m.group('fd')
        if not m.group('ft'):
            start = startf + ' 00:00:00'
        esimene = dt.strptime(start, ISOFMT)
        end = m.group('sd') or startf
        if not m.group('st'):
            end = end + ' 23:59:59'
        teine = dt.strptime(end, ISOFMT)
        r = [esimene, teine]
    return {'value_type': type(r[0]), 'min_value': min(r), 'max_value': max(r)}


def make_search(value, key, args):
    if 'min_value' in args.keys() and 'max_value' in args.keys():
        if args['value_type'] == type(1):
            value = int(value)
        elif key in ['kuupaev', 'date', 'date_of_speech']:
            print(args['value_type'])
            value = dt.strptime(value, ISOFMT)
        if value >= args['min_value'] and value <= args['max_value']:
            return True
    return False


def iter_items(parser, key, args):
    out = []
    lisa = False
    lisa_speech = False
    runkeys = []
    values = []
    for prefix, event, value in parser:
        # print('===')
        # print('iter_items---prefix: {}'.format(prefix))
        # print('iter_items---event: {}'.format(event))
        # print('iter_items---value: {}'.format(value))
        # print('-' * 3)
        if 'speech_data' in prefix:
            if '.' in prefix:
                runkey = prefix.split('.')[-1]
            else:
                runkey = None
            # print('runkey : {}'.format(runkey))
            if event in ['string', 'null', 'number']:
                runkeys.append(runkey)
                values.append(value)
                if key == runkey:
                    lisa = make_search(value, key, args)
                    # print('lisa: {}'.format(lisa))
            elif event == 'end_map':
                if lisa:
                    out.append(
                        {'speech_data':
                        dict(zip(runkeys, values))
                         }
                    )
                    lisa_speech = True
                    lisa = False
                # print('LISA OUT: {}'.format(out))
        elif 'speech' in prefix and not 'speech_data' in prefix:
            # print('Speech in prefix !')
            if event in ['start_array']:
                konesisu = []
            elif event in ['string']:
                konesisu.append(value)

            elif event == 'end_array':
                if lisa_speech:
                    out[-1]['speech'] = konesisu
                    lisa_speech = False
                runkeys = []
                values = []

                # print('OUT: {}'.format(out))



    # print('ITER ITEMS OUT: {}'.format(out))
    return out


def returnparser():
    parser = argparse.ArgumentParser(
        description='Read json file'
    )
    parser.add_argument('infile')
    parser.add_argument('outfile')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-k', '--kuupaev', type=parseDates)
    group.add_argument('-j', '--jrk', type=parseNumList)
    return parser


def limit(text, lim=30):
    try:
        if len(text) > lim:
            return text[:lim-1] + '...'
    except TypeError:
        return text
    return text


def main(p: argparse.ArgumentParser):
    args = p.parse_args()
    valuerange = {}
    if args.kuupaev:
        # k = 'kuupaev'
        # k = 'date'
        k = 'date_of_speech'
        print('Valitud kuupäev(ad): {}'.format(args.kuupaev))
        valuerange = args.kuupaev
    if args.jrk:
        k = 'jrk'
        print('Valitud number või vahemik: {}'.format(args.jrk))
        valuerange = args.jrk

    print('k = {}'.format(k))

    with open(args.infile, 'rb') as infile:
        parser = ijson.parse(infile)
        # print('parser = {}'.format(parser))
        items = [x for x in iter_items(parser, k, valuerange)]
        # items = [x for x in iter_items(parser, k)]
        # print('items = {}'.format(items))
    with open(args.outfile, 'w') as outfile:
        json.dump(items, outfile, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)
