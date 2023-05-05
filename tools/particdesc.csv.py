#!/usr/bin/env python3
"""
Usage:

"""
import argparse
import os.path
import csv

from lxml import etree
from copy import deepcopy

def person(datarow):
    root = etree.fromstring('<person xml:id="{}" />'.format(datarow['name_std']))
    persName = etree.SubElement(root, 'persName')
    surname = etree.SubElement(persName, 'surname')
    surname.text = datarow['name_last']
    forename = etree.SubElement(persName, 'forename')
    forename.text = datarow['name_first']
    birth = etree.SubElement(root, 'birth')
    birth.set('when', datarow['birth'])
    return root

def


def read_csv(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            r = person(row)
            print(etree.tostring(r, encoding="unicode", pretty_print=True))

def returnparser():
    parser = argparse.ArgumentParser(
        description='ParlaMint csv metadata to TEI'
    )
    parser.add_argument('infile')
    # parser.add_argument('outpath')
    # parser.add_argument('-f', '--fn', default='ParlaMint-EE')
    return parser

def main(p: argparse.ArgumentParser):
    args = p.parse_args()
    xmlext = '.xml'
    read_csv(args.infile)
    # out = etree.tostring(root, pretty_print=True, encoding='unicode', doctype=xml_doctype)
    # with open(os.path.join(args.outpath, args.fn + xmlext), 'w') as xf:
    #     xf.write(out)


if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)
