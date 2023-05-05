#!/usr/bin/env python3
"""
Convert analysed xml file to vert format
<<<<<<< HEAD
"""
import argparse
from lxml import etree

=======

Subcorpus is riigikogu koosseis (#parla.term)
text is riigikogu istung (#parla.sitting)
"""
import argparse
import os
from lxml import etree

class KorpusElement():
    tag = 'element'
    def __init__(self, content = None):
        self.content = content or []

    def make_vert(self):
        starttag = '<{}>'.format(self.tag)
        endtag = '</{}>'.format(self.tag)
        self.content.insert(0, starttag)
        self.content.append(endtag)


class Korpus(KorpusElement):
    tag = 'corpus'
    def __init__(self, vert_filename, content=None):
        super().__init__(content)
        self.vert_filename = vert_filename


class KorpusText():
    def __init__(self, vert_filename, content):
        self.vert_filename = vert_filename
        self.content = content
        self.tag = 'text'

class Utterance():
    def __init__(self, content):
        self.tag = 'u'
        self.content = content

class Word():
    def __init__(self, form: str, lemma: str):
        self.form = form
        self.lemma = lemma



>>>>>>> dev
def returnparser():
    parser = argparse.ArgumentParser(
        description='Analysed xml file to vert format'
    )
<<<<<<< HEAD
    parser.add_argument('infile')
=======
    parser.add_argument('inpath')
>>>>>>> dev
    parser.add_argument('outfile')
    return parser

def main(p: argparse.ArgumentParser):
    args = p.parse_args()
<<<<<<< HEAD
    corpus = etree.parse(args.infile)
    print(corpus)
=======
    ifiles = [os.path.join(args.inpath, x) for x in os.listdir(args.inpath)]
    print(ifiles)
    corpora = []
    for i in ifiles:
        corpora.append(etree.parse(i))
    print(corpora)
    # textcorpus = etree.tostring(corpus, pretty_print=True, encoding='unicode')
    # print(textcorpus)
>>>>>>> dev

if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)