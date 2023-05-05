#!/usr/bin/env python3
"""
Compare extents, fill necessary
"""
import argparse
import os
from lxml import etree

# EXT =  './/TEI/teiHeader/extent'
EXT =  './/{*}extent'
SOURCEDESC = './/{*}sourceDesc/{*}bibl'

def split_units(text: str):
    out = {}
    out['amount'], out['unit'] = text.split()
    return out

def compare_data(ana: etree._Element, xml: etree._Element,
                 tofind: str, changexml: bool = True):
    if changexml:
        model = ana.find(tofind)
        variable = xml.find(tofind)
        changed = xml
    else:
        model = xml.find(tofind)
        variable = ana.find(tofind)
        changed = ana

    for n, i in enumerate(model):
        if variable[n].text != i.text:
            variable[n].text = i.text
        content = i.text
        print('model content: {}'.format(content))
        # Let's assume same structure
        print('var content: {}'.format(variable[n].text))

    uusxml = etree.tostring(changed, pretty_print=True, encoding='unicode')
    return uusxml
    # print(uusxml)



def returnparser():
    parser = argparse.ArgumentParser(
        description='Compare xml files, fill extents'
    )
    parser.add_argument('anafile')
    parser.add_argument('xmlfile')
    return parser

def main(p: argparse.ArgumentParser):
    args = p.parse_args()
    # check filenames
    anadoc = etree.parse(args.anafile)
    xmldoc = etree.parse(args.xmlfile)
    ananame = os.path.splitext(os.path.basename(args.anafile))[0]
    xmlname = os.path.splitext(os.path.basename(args.xmlfile))[0]
    # print('ana :', os.path.splitext(os.path.basename(args.anafile))[0])
    # print('xml :', os.path.splitext(os.path.basename(args.xmlfile))[0])
    # print(anadoc)
    # print(xmldoc)
    # anadoc = etree.getroot(anadoc)
    if ananame != xmlname + '.ana':
        raise NameError('File names do not match!')
    # a = anadoc.find(EXT)
    # for i in a:
    #     print(split_units(i.text))
    # print(a)
    # b = xmldoc.find(EXT)
    # for i in b:
    #     print(split_units(i.text))
    # print(b)

    uusxml = compare_data(anadoc, xmldoc, EXT)
    uusana = compare_data(anadoc, xmldoc, SOURCEDESC, False)

    with open(args.xmlfile, 'w') as f:
        f.write(uusxml)
    with open(args.anafile, 'w') as f:
        f.write(uusana)

if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)

