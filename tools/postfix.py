#!/usr/bin/env python3
"""
Post-process fixings
"""
import argparse
import os.path
from pathlib import Path

def read_xmlfile(filename: str):
    pass



def read_path(path: str, ending: str):
    p = Path(path)
    koik_failid = [x for x in p.iterdir() if x.is_file()]
    olulised_failid = [x for x in koik_failid if x.name.endswith(ending)]
    return olulised_failid


def fn2data(line: str):
    tyvi, kuup, andmed = line.split('_')
    return {'filename':'_'.join([tyvi, kuup]), 'data': andmed}

def pivot_data(ilist: list):
    out = []
    while ilist:
        a = ilist.pop(0)
        if out:
            if a['filename'] in [x['filename'] for x in out]:
                out[-1]['data'].append(a['data'])
            else:
                out.append({'filename': a['filename'], 'data': [a['data']]})
        else:
            out.append({'filename': a['filename'], 'data': [a['data']]})
    return out

def read_log(logfile):
    with open(logfile) as f:
        all_loglines = [x.strip() for x in f.readlines()]
    warns = [x for x in all_loglines if x.startswith('WARN: skipping segment without sentences') ]
    fns = [fn2data(x.split()[-1]) for x in warns]
    return fns


def returnparser():
    parser = argparse.ArgumentParser(
        description='Postfix'
    )
    parser.add_argument('inpath')
    parser.add_argument('outpath')
    parser.add_argument('-l', '--logfile')
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    return parser

def main(p: argparse.ArgumentParser):
    args = p.parse_args()

    if args.logfile:
        logs = read_log(args.logfile)
        filelog = pivot_data(logs)
        # for i in filelog:
        #     print(i)

    # print(read_path(args.inpath, 'ana.xml'))
    failid = read_path(args.inpath, 'ana.xml')
    print(len(failid))

    if args.debug:
        print(filelog[0])


if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)