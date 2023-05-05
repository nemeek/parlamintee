#!/usr/bin/env python3
"""
Read json file, write chunks of json file according to params
"""
import argparse
import ijson
# import json
import re
# import lxml
# import datetime
from datetime import datetime as dt
from lxml import etree

from estnltk import Text
from estnltk.taggers import GTMorphConverter, NerTagger, WordLevelNerTagger

nertagger = NerTagger()
word_level_ner = WordLevelNerTagger()

RS = '¤'

ISOFMT='%Y-%m-%d %H:%M:%S'
ISOSHORT='%Y-%m-%d'
DOTFORMAT='%d.%m.%Y'
NUMBERKEYS = ['jrk', 'haaled']
DATEPATTERN = re.compile(r'(?P<fd>[12][09][0129]\d[-][01]\d[-][0-3]\d(?P<ft> [0-2]\d:[0-5]\d:[0-5]\d)?)(?: - (?P<sd>[12][09][0129]\d[-][01]\d[-][0-3]\d(?P<st> [0-2]\d:[0-5]\d:[0-5]\d)?))?')
NUMBERPATTERN = re.compile(r'(\d{1,4})(?: ?- ?(\d{1,4}))?')
FSPATTERN = re.compile(r'([.!])([^ ][A-Ü])')

XMLNSNS = "http://www.w3.org/XML/1998/namespace"
XMLNS = "http://www.tei-c.org/ns/1.0"

NSMAP = {None: XMLNS, 'xml': XMLNSNS}
ROOT = etree.Element('teiCorpus', nsmap=NSMAP, attrib={etree.QName(XMLNSNS, 'lang'):'{}'.format('et')})


def _list2attr(variants: list) -> str:
    uus = list(set([x for x in variants if x]))
    uus.sort()
    return '|'.join(uus)


def nametype(txt: str):
    m = {'LOC':'place', 'PER':'person', 'ORG':'org'}
    return m[txt]

def build_syntax_xml(parent: etree._Element, text: Text):
    gt_converter = GTMorphConverter()
    parent.text = None
    text.tag_layer(['morph_analysis','words','clauses'])
    gt_converter.tag(text)
    word_level_ner.tag(text)
    texts = text['sentences']
    for lt in texts:
        s = etree.SubElement(parent, 's')
        for t in lt:
            lemmalist = t.gt_morph_analysis.lemma
            poslist = t.gt_morph_analysis.partofspeech
            formlist = [x.replace(' ', '.') for x in t.gt_morph_analysis.form]
            rootlist = t.gt_morph_analysis.root
            wname = t.wordner.nertag
            # print(t.text)
            # print (lemmalist)
            # print(wname)
            # print(rootlist)
            # print(endlist)
            # print('---')
            etag = 'w'
            if etag == 'w' and _list2attr(poslist) == 'Z':
                etag = 'pc'
            e = etree.Element(etag, lemma=_list2attr(lemmalist),
                                    pos=_list2attr(poslist),
                                    msd='{}{}{}'.format(_list2attr(rootlist), RS, _list2attr(formlist))
                              )
            e.text = t.text
            if wname.startswith('B'):
                n = etree.Element('name', type=nametype(wname[2:]))
                n.append(e)
                s.append(n)
            elif wname.startswith('I'):
                n.append(e)
                s.append(n)
            else:
                s.append(e)
    return parent


def build_p_xml(parent: etree._Element, text: Text):
    gt_converter = GTMorphConverter()
    parent.text = None
    text.tag_layer(['morph_analysis','words','clauses'])
    gt_converter.tag(text)
    #nertagger.tag(text)
    word_level_ner.tag(text)
    texts = text['sentences']
    for lt in texts:
        s = etree.SubElement(parent, 's')
        for t in lt:
            # n = None
            lemmalist = t.gt_morph_analysis.lemma
            poslist = t.gt_morph_analysis.partofspeech
            formlist = [x.replace(' ', '.') for x in t.gt_morph_analysis.form]
            rootlist = t.gt_morph_analysis.root
            # endlist = t.gt_morph_analysis.ending
            wname = t.wordner.nertag
            # print(t.text)
            # print (lemmalist)
            # print(wname)
            # print(rootlist)
            # print(endlist)
            # print('---')
            etag = 'w'
            if etag == 'w' and _list2attr(poslist) == 'Z':
                etag = 'pc'
            e = etree.Element(etag, lemma=_list2attr(lemmalist),
                                    pos=_list2attr(poslist),
                                    msd='{}{}{}'.format(_list2attr(rootlist), RS, _list2attr(formlist))
                              )
            e.text = t.text
            if wname.startswith('B'):
                n = etree.Element('name', type=nametype(wname[2:]))
                n.append(e)
                s.append(n)
            elif wname.startswith('I'):
                n.append(e)
                s.append(n)
            else:
                s.append(e)
    return parent

def birthdate_from_id(id: str):
    kuupnr = id.split('_')[-1]
    date = '{}-{}-{}'.format(kuupnr[0:4], kuupnr[4:6], kuupnr[6:8])
    return date


def get_persondata(item: dict):
    # names = item['esineja_std'].split(' ')
    # names = item['name_orig'].split(' ')
    print('item: {}'.format(item))
    surname = None
    roleName = None
    sex = None
    sexvalue = None
    initial = None
    # if len(names) > 1:
    #     surname = names[-1]
    #     if len(names[0]) == 1:
    #         initial = names[0]
    # else:
    #     roleName = names[0]
    # synnikuup = birthdate_from_id(item['id'])

    # try:
    #    dateKuup = dt.strptime(synnikuup, DOTFORMAT)
    # except TypeError:
    #    dateKuup = dt.strptime('01.01.1901', DOTFORMAT)
    # personid = '{}{}'.format(''.join(names), dateKuup.year)
    # personid = item['id']
    # birthdate = dateKuup.strftime(ISOSHORT)
    birthdate = synnikuup

    if 'sugu' in item and item['sugu'] == 'mees':
        sex = 'male'
        sexvalue = 'M'
    elif 'sugu' in item and item['sugu'] == 'naine':
        sex = 'female'
        sexvalue = 'F'
    else:
        sex = None
        sexvalue = None

    out = {'personid': personid, 'surname':surname, 'initial': initial, 'roleName': roleName,
           'sex': sex, 'sexvalue':sexvalue, 'synnikuup': synnikuup, 'birthdate': birthdate}
    return out


def item2tei(item: dict, idd: int,
             analyse: bool = False, syntax: bool = False):
    # TODO: syntax
    idd +=1
    t = etree.Element('TEI', nsmap=NSMAP, attrib={etree.QName(XMLNSNS, 'id'): '{}'.format(idd)})
    h = etree.Element('teiHeader')
    t.append(h)
    text = etree.Element('text')
    body = etree.Element('body')
    div = etree.Element('div')
    u = etree.Element('u', who='#{}'.format(get_persondata(item)['personid']))

    div.append(u)
    body.append(div)
    text.append(body)
    t.append(text)
    parad = paras(item['text'])
    if analyse:
        for i in parad:
            u.append(build_p_xml(i, Text(i.text)))
    elif syntax:
        for i in parad:
            u.append(build_syntax_xml(i, Text(i.text)))
    else:
        for i in parad:
            u.append(i)
    return t


def paras(tekst: str, delim: str = None):
    """

    :param tekst:
    Sisendtekst
    :return:
    Paragrafide (<p>) list koos tekstiga.
    """
    # Find para delimiters
    pout = []
    if not delim:
        delim = '$'
        tekst = FSPATTERN.sub(r'\1{}\2'.format(delim), tekst)
    out = tekst.split(delim)
    for i in out:
        p = etree.Element('p')
        p.text = i
        pout.append(p)
    return pout


def make_corpus(root: etree._ElementTree, header: etree.Element, items,
                analyse: bool = False, syntax: bool = False):
    root.append(header)
    pd = etree.Element('particDesc')
    header.append(pd)
    lp = etree.Element('listPerson')
    pd.append(lp)
    for n,i in enumerate(items):
        root.append(item2tei(i, n, analyse, syntax))
        pdata = get_persondata(i)
        persoonid = [x.attrib['{{{}}}id'.format(XMLNSNS)] for x in root.findall('*//listPerson/person')]
        # print(persoonid)
        person = etree.Element('person', attrib={etree.QName(XMLNSNS, 'id'): '{}'.format(pdata['personid'])})
        if pdata['personid'] not in persoonid:
            lp.append(person)
            pn = etree.Element('persName')
            person.append(pn)
            if 'surname' in pdata.keys() and pdata['surname']:
                #print ('surname in i.keys()')
                sn = etree.Element('surname')
                sn.text = pdata['surname']
                pn.append(sn)
            elif 'roleName' in pdata.keys() and pdata['roleName']:
                rn = etree.Element('roleName')
                rn.text = pdata['roleName']
                pn.append(rn)
            if 'sex' in pdata.keys() and pdata['sex']:
                sex = etree.Element('sex', attrib={'value': pdata['sexvalue']})
                sex.text = pdata['sex']
                person.append(sex)
            if 'synnikuup' in pdata.keys() and pdata['synnikuup']:
                sk = etree.Element('birth', attrib={'when':pdata['birthdate']})
                sk.text = pdata['synnikuup']
                person.append(sk)
    return root


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
        elif key == 'kuupaev':
            value = dt.strptime(value, ISOFMT)
        if value >= args['min_value'] and value <= args['max_value']:
            return True
    return False


def iter_items(parser):
    out = []
    lisa = False
    runkeys = []
    values = []
    for prefix, event, value in parser:

        if '.' in prefix:
            runkey = prefix.split('.')[1]
        else:
            runkey = None
        if event in ['string','null','number']:
            runkeys.append(runkey)
            values.append(value)
            lisa = True
        elif event == 'end_map':
            if lisa:
                out.append(dict(zip(runkeys, values)))
                lisa = False
            runkeys = []
            values = []
    return out


def returnparser():
    parser = argparse.ArgumentParser(
        description='Read json file'
    )
    parser.add_argument('infile')
    parser.add_argument('outfile')

    groupa = parser.add_mutually_exclusive_group()
    groupa.add_argument('-a', '--analysis', action='store_true')
    groupa.add_argument('-s', '--syntax', action='store_true')

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
    if args.analysis: # test analysis
        print('On analüüs!')
    if args.kuupaev:
        k = 'kuupaev'
        print('Valitud kuupäev(ad): {}'.format(args.kuupaev))
        valuerange = args.kuupaev
    if args.jrk:
        k = 'jrk'
        print('Valitud number või vahemik: {}'.format(args.jrk))
        valuerange = args.jrk

    with open(args.infile, 'rb') as infile:
        parser = ijson.parse(infile)
        items = [x for x in iter_items(parser)] #, k, valuerange)]
        #sitems = item2tei(items)
    h = etree.Element('teiHeader')
    corpus = make_corpus(ROOT, h, items, analyse=args.analysis, syntax=args.syntax)
    with open(args.outfile, 'w') as outfile:
        outfile.write(etree.tostring(corpus,
                                     encoding='unicode', pretty_print=True)
                      )


if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)
