#!/usr/bin/env python3
"""
Compare files, json, xml and ana.xml
"""
import argparse
import os
import csv

from lxml import etree

EXT =  './/TEI/teiHeader/extent'
EXT =  './/{*}extent'

def makeline(json, ana, xml, anapath, xmlpath, outfile):
    print(json)
    print(os.path.realpath(os.path.join(anapath, ana)))
    out = '{};{};{}\n'.format(
        json,
        os.path.isfile(os.path.realpath(os.path.join(anapath, ana))),
        os.path.isfile(os.path.realpath(os.path.join(xmlpath, xml))),
    )
    with open(outfile, 'a') as f:
        f.write(out)


def returnparser():
    parser = argparse.ArgumentParser(
        description='Compare json files with xml and ana.xml'
    )
    parser.add_argument('jsonfile')
    parser.add_argument('anapath')
    parser.add_argument('xmlpath')
    parser.add_argument('-s', '--stat')
    return parser

def main(p: argparse.ArgumentParser):
    args = p.parse_args()
    # check filenames

    # anadoc = etree.parse(args.anafile)
    # xmldoc = etree.parse(args.xmlfile)

    filename = os.path.splitext(os.path.basename(args.jsonfile))[0]
    print(filename)
    anafilename = filename + '.ana.xml'
    xmlfilename = filename + '.xml'
    fullanafilename = os.path.join(args.anapath, anafilename)
    fullxmlfilename = os.path.join(args.xmlpath, xmlfilename)

    if args.stat:
        makeline(filename, anafilename, xmlfilename,
                 args.anapath, args.xmlpath, args.stat)

    # print(filename, fullanafilename, fullxmlfilename)

    # ananame = os.path.splitext(os.path.basename(args.anafile))[0]
    # xmlname = os.path.splitext(os.path.basename(args.xmlfile))[0]

    # print('ana :', os.path.splitext(os.path.basename(args.anafile))[0])
    # print('xml :', os.path.splitext(os.path.basename(args.xmlfile))[0])
    # print(anadoc)
    # print(xmldoc)
    # anadoc = etree.getroot(anadoc)
    # if ananame != xmlname + '.ana':
    #     raise NameError('File names do not match!')
    # a = anadoc.find(EXT)
    # for i in a:
    #     print(i.text)
    # print(a)
    # b = xmldoc.find(EXT)
    # for i in b:
    #     print(i.text)
    # print(b)

if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)

