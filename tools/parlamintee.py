#!/usr/bin/env python3
"""
parlamintee.py
Usage:
./parlamintee.py ../data/data-test/ParlaMint-EE_2015-01-12.json ../data/new-testdata/
./parlamintee.py -x ../data/data-test/ParlaMint-EE_2015-01-12.json ../data/data-2022-10-18/
./parlamintee.py -ax ../data/json/ParlaMint-EE_2012-01-25.json ../data/data-2022-10-25

Validate:
xmllint --noout --relaxng Schema/ParlaMint-TEI.rng ~/GIT/parlamint/data/data-2022-10-18/ParlaMint-EE_2015-01-12.xml
jing Schema/ParlaMint-TEI.ana.rng ~/GIT/parlamint/data/data-2022-10-18/ParlaMint-EE_2015-01-12.ana.xml

Syntax:
 cat ParlaMint-EE_20*ana*|grep '<link '|sed -r 's/^[[:space:]]+//g'|cut -d' ' -f 2|sort|uniq -c|sort -nr
UD Estonian:
https://universaldependencies.org/et/index.html

"""
import argparse
import datetime
import json
import os.path
import sys
import re

from lxml import etree

from estnltk import Text
from estnltk.taggers import WordLevelNerTagger
from estnltk.layer_operations import split_by
from estnltk.taggers.syntax.stanza_tagger.stanza_tagger import StanzaSyntaxTagger

## --- Global variables and settings ---
REFERENCE_DATE = '2019-10-31'
COVID_DATE = '2019-11-01'
NL = '\n'
CONLLU_EXT = 'conllu'
VERT_EXT = 'vert'
XMLNS = 'http://www.w3.org/XML/1998/namespace'
NSMAP = {'xml': XMLNS}

stanza_tagger_sent = StanzaSyntaxTagger(input_type='sentences',
                                        output_layer='stanza_syntax_sent',
                                        depparse_path='',)
word_level_ner = WordLevelNerTagger()
rk_labels = [
    {'id': 'parliament.RK11', 'label': 'XI Riigikogu', 'year': '2007'},
    {'id': 'parliament.RK12', 'label': 'XII Riigikogu', 'year': '2011'},
    {'id': 'parliament.RK13', 'label': 'XIII Riigikogu', 'year': '2015'},
    {'id': 'parliament.RK14', 'label': 'XIV Riigikogu', 'year': '2019'},
]
session_labels = [
    {'label': 'I regular session', 'id': 'rs1'},
    {'label': 'II regular session', 'id': 'rs2'},
    {'label': 'III regular session', 'id': 'rs3'},
    {'label': 'IV regular session', 'id': 'rs4'},
    {'label': 'V regular session', 'id': 'rs5'},
    {'label': 'VI regular session', 'id': 'rs6'},
    {'label': 'VII regular session', 'id': 'rs7'},
    {'label': 'VIII regular session', 'id': 'rs8'},
    {'label': 'IX regular session', 'id': 'rs9'},
    {'label': 'extraordinary session', 'id':'exs'}
]
RESP_LIST = [{'name':'Martin Mölder', 'orcid': '0000-0002-9701-1771'},
             {'name':'Neeme Kahusk', 'orcid': 'https://orcid.org/0000-0003-0511-5854'},
             {'name':'Kadri Vider', 'orcid': '0000-0003-0966-8341'},
             {'lang': 'en', 'resp':'Data retrieval and conversion to Parla-CLARIN TEI XML'}
             ]
CLARIN_ERIC = [
    {'element': 'orgName', 'text': 'CLARIN ERIC teadustaristu', 'lang': 'et'},
    {'element': 'orgName', 'text': 'CLARIN ERIC research infrastructure', 'lang': 'en'}
]
PUBLISHER_HANDLE = {
    'subtype':'handle',
    'type':'URI',
    'text':'http://hdl.handle.net/11356/1431'
}
CC_BY_40_XML = """
<availability status="free">
<licence>http://creativecommons.org/licenses/by/4.0/</licence>
<p xml:lang="en">This work is licensed under the <ref 
target="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</ref>.</p>
</availability>
"""
BIBL = """<bibl>
          <title type="main" xml:lang="et">Riigikogu stenogrammid</title>
        </bibl>"""
PROJECT_DESC = """ <projectDesc>
        <p xml:lang="en">
          <ref target="https://www.clarin.eu/content/parlamint">ParlaMint</ref>
        </p>
      </projectDesc>
"""
RIIGIKOGU_SETTING = """<setting><name type="org">Riigikogu</name>
          <name type="address">Lossi plats 1a</name>
          <name type="city">Tallinn</name>
          <name type="country" key="EE">Estonia</name></setting>"""


## --- Classes ---
class DatesNotMatch(Exception):
    "Raised when dates do not match"
    pass

class RefOrCovid(Exception):
    "Raised when covid or ref is in conflict"
    pass

class SPData():
    def __init__(self, *args):
        self.parliament_election_year = ""
        self.date_of_speech = datetime.datetime.today().isoformat(' ')
        self.speaker_id = ""
        self.speaker_first_name = "Eesnimi"
        self.speaker_last_name = "Perenimi"
        self.mp_chair = 0
        self.mp_deputy_chair = 0
        self.mp_regular = 0
        self.mp_governing_party = 0
        self.guest = 0
        self.government_minister = 0
        self.speaker_gender = 'teadmata'
        self.speaker_birth_date = datetime.datetime.today().isoformat(' ')
        self.parliamentary_group = None
        self.political_party = None
        self.electoral_list = None
        self.transcript_url = None
        self.session = 'JAMA'
        self.sitting_type = None
        self.general_header = None
        self.agenda_item = None

        self.__dict__ = {k:v for (k,v) in zip(vars(self), args)}

    def json(self):
        v = vars(self)
        return v


class Speech():
    """There is one utterance (<u/>) for every speech. Every speech is divided into paragraphs,
    they are encoded as <seg/>.
    """
    utteranceCounter = 0
    u = 'U'
    filename = None
    outpath = None
    xml_doctype = '<?xml version="1.0" encoding="UTF-8"?>'
    wordCounter = 0
    def __init__(self, metadata: SPData, data: list = []):
        self.metadata = metadata
        # TODO: take account real utterance
        Speech.utteranceCounter +=1
        self.utterance = Speech.utteranceCounter
        self.data = data # List of texts
        if Speech.filename:
            self.fn = os.path.splitext(os.path.basename(Speech.filename))[0]
            self.fnd = self.fn[-10:-1]
        else:
            self.fn = None
            self.fnd = None
        self.nltexts = [] # Speech data analysed with EstNLTK
        self.utid = None
        self.utid = '{}_{}{}'.format(self.fn, Speech.u, self.utterance)
        self.txt_file = os.path.join(Speech.outpath, self.fn) + '.' + 'txt'
        self.conllu_file = os.path.join(Speech.outpath, self.fn) + '.' + CONLLU_EXT
        self.vert_file = os.path.join(Speech.outpath, self.fn) + '.' + VERT_EXT
        self.notes = None
        self.xmlcontent = []
        self.shortdata = []

    def make_nltexts(self, notelist = None):
        for n,i in enumerate(self.data):
            if "'" in i:
                self.data[n] = i.replace("'", '"')
        try:
            local_notelist = list(notelist)
        except TypeError:
            local_notelist = None
        if local_notelist:
            self.shortdata = []
            self.notes = []
            for i in self.data:
                nl = make_notes(i, local_notelist)
                self.notes.append(nl)
                self.shortdata.append(txt_minus_notes(i, nl))
            textual_data = self.shortdata
        else:
            textual_data = self.data
        self.nltexts = [
                ('{}-P{}'.format(self.utid, n + 1),
                 [
                     ('{}-P{}.{}'.format(self.utid, n+1, m+1), y) for m, y in enumerate(
                     split_by(analyse(
                         Text(x)
                     ),
                     'sentences'))
                  ]
                 ) for n,x in enumerate(textual_data)
                ]

    def xml(self, notelist: list, anal: bool = False):

        sisu = []
        if not self.shortdata:
            self.make_nltexts(notelist)
        note = None
        u = None
        if not self.metadata.speaker_id:
            note = etree.Element('note', {'type':'comment'})
            note.text = ' '.join(self.data)
        else:
            note = etree.Element('note', {'type':'speaker'})
            note.text = '{} {}'.format(self.metadata.speaker_first_name,
                                       self.metadata.speaker_last_name)
            u = etree.Element('u')
            u.set('who', '#{}'.format(self.metadata.speaker_id))
            u.set('{http://www.w3.org/XML/1998/namespace}id', self.utid)
            u.set('ana', speaker_type(self.metadata.mp_chair, self.metadata.mp_deputy_chair,
                                       self.metadata.mp_regular, self.metadata.mp_governing_party,
                                       self.metadata.government_minister, self.metadata.guest)
                   )
            for num, i in enumerate(self.nltexts):
                fullnote = False
                short_text = ' '.join([x[-1].text for x in i[-1]])
                no_of_words_in_seg = len(short_text.split())
                Speech.wordCounter = Speech.wordCounter + no_of_words_in_seg
                seg_text = self.data[num]
                nnn = make_notes(seg_text, notelist)
                if nnn:
                    # print(nnn)
                    if len(nnn) == 1 and nnn[0]['algus'] == 0 and nnn[0]['ots'] == nnn[0]['vahe']:
                        elnote = etree.SubElement(u, 'note')
                        elnote.text = nnn[0]['note']
                        fullnote = True
                        # break
                if anal:
                    seg = etree.Element('seg')
                    seg.set('{http://www.w3.org/XML/1998/namespace}id', i[0])
                    offset = 0

                    for s in i[-1]:
                        sent = etree.SubElement(seg, 's')
                        sent.set('{http://www.w3.org/XML/1998/namespace}id', s[0])
                        a = stanza_analysis(s[-1])
                        wcount = 0

                        sentlist = [(0, s[0], None, None)]
                        # print(3 * '-- --')
                        for n,w in enumerate(a):
                            wcount +=1
                            if w.lemma == "'" and w.wordner.nertag != 'O':
                                w.wordner.nertag = 'O'
                                print(a)
                                print(n, w.text)
                            # print('W: {}'.format(w.text))
                            if w.wordner.nertag != 'O':
                                if wcount == 1 or (not a[n-1].wordner.nertag.startswith('B')) and w.wordner.nertag.startswith('I'):
                                    w.wordner.nertag = 'B' + w.wordner.nertag[1:]
                                try:
                                    position, type = w.wordner.nertag.split('-')
                                except:
                                    print()
                                    print(w)
                                    print(w.wordner.nertag)
                                    raise
                                if position == 'B':
                                    name = etree.SubElement(sent, 'name')
                                try:
                                    name.set('type', type)
                                except:
                                    print('{}.{}'.format(s[0], wcount))
                                    print('Katkestav lause:')
                                    print(s)
                                    raise
                                word = etree.SubElement(name, wordtag(w))
                            else:
                                word = etree.SubElement(sent, wordtag(w))
                            wordid = '{}.{}'.format(s[0], wcount)
                            word.set('{http://www.w3.org/XML/1998/namespace}id', wordid)
                            if word.tag == 'w':
                                word.set('lemma', w.lemma.replace(' ',''))
                            if wcount < len(a):
                                if w.end == a[wcount].start:
                                    word.set('join', 'right')
                            if w.feats:
                                word.set('msd', '{}={}|{}'.format('UPosTag', w.upostag, features(w.feats)))
                            else:
                                word.set('msd', '{}={}'.format('UPosTag', w.upostag))
                            word.set('pos', w.xpostag)
                            word.text = w.text.replace(' ', '')
                            if self.notes[num]:
                                if self.notes[num][0]['algus'] == 1 + w.end + offset:
                                    nt = etree.SubElement(sent, 'note')
                                    nt.text = self.notes[num][0]['note']
                                    offset = 1 + offset + self.notes[num][0]['vahe']
                                    self.notes[num].pop(0)
                            sentlist.append((wcount, wordid, w.head, w.deprel))
                        offset = offset + w.end +1
                        linkgrp = etree.SubElement(sent, 'linkGrp')
                        linkgrp.set('targFunc', 'head argument')
                        linkgrp.set('type', 'UD-SYN')
                        for l in [x for x in sentlist if x[-1]]:
                            link = etree.SubElement(linkgrp, 'link')
                            link.set('ana', '{}:{}'.format('ud-syn', l[-1].replace(':', '_')))
                            link.set('target', '#{} #{}'.format([x[1] for x in sentlist if x[0] == l[2]][0], l[1]))
                else:
                    # We don't do morph analysis
                    seg_text = self.data[num]

                    if ' & ' in seg_text:
                        seg_text = seg_text.replace(' & ', ' &amp;')

                    if nnn:
                        if not (len(nnn) == 1 and nnn[0]['algus'] == 0 and nnn[0]['ots'] == nnn[0]['vahe']):
                            seg_as_str = notes_to_xml(seg_text, nnn, '<seg>', '</seg>')
                            # print(seg_as_str)
                            seg = etree.fromstring(seg_as_str)
                            seg.set('{http://www.w3.org/XML/1998/namespace}id', i[0])
                        else:
                            pass
                    else:
                        seg = etree.Element('seg')
                        seg.set('{http://www.w3.org/XML/1998/namespace}id', i[0])
                        seg.text = seg_text

                u.append(seg)

                try:
                    if not fullnote:
                        u.append(seg)
                except:
                    pass


        if note is not None:
            sisu.append(note)
        if u is not None:
            sisu.append(u)
        return sisu

    def text(self):
        """
        Suitable for output text only.
        :return:
        Text where textID is separated with \t from the text itself. All paragraphs are together.
        """
        outtext = '{}\t{}'.format(self.utid, ' '.join([x.text for x in self.nltexts]))
        with open(self.txt_file, 'a') as cf:
            cf.write(outtext + NL)

    def conllu(self):
        if not self.nltexts:
            self.make_nltexts()
        content = '# {} = {}'.format('newdoc id', self.utid)
        for i in self.nltexts:
            content = content + NL + '# {} = {}'.format('newpar id', i[0])
            for s in i[-1]:
                content = content + NL + '# {} = {}'.format('sent_id', s[0])
                content = content + NL + '# {} = {}'.format('text', s[-1].text)
                a = stanza_analysis(s[-1])
                for w in a:
                    lisa = 'NER={}'.format(w.wordner.nertag)
                    if w.id < len(a):
                        # print('jajah!')
                        if w.end == a[w.id].start:
                            # print('Parandan!')
                            lisa = 'NER={}|{}'.format(w.wordner.nertag, 'SpaceAfter=No')

                    content = content + NL + '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                        w.id, w.text, w.lemma,
                        w.upostag, w.xpostag,
                        features(w.feats) or '_', w.head,
                        w.deprel, '_', lisa
                    )
                content = content + NL
        with open(self.conllu_file, 'a') as cf:
            cf.write(content + NL)

    def vert(self):
        self.make_nltexts()
        content = '# {} = {}'.format('newdoc id', self.utid)
        for i in self.nltexts:
            content = content + NL + '# {} = {}'.format('newpar id', i[0])
            for s in i[-1]:
                content = content + NL + '# {} = {}'.format('sent_id', s[0])
                content = content + NL + '# {} = {}'.format('text', s[-1].text)
                a = stanza_analysis(s[-1])
                for w in a:
                    content = content + NL + '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                        w.id, w.text, w.lemma,
                        w.upostag, w.xpostag,
                        features(w.feats), w.head,
                        w.deprel, '_', w.wordner.nertag
                    )
                content = content + NL
        with open(self.vert_file, 'a') as cf:
            cf.write(content + NL)

    def __repr__(self):
        return 'Speech no. {} of {}'.format(self.utterance, self.fn)


class SpeechEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Speech):
            return {
                "speech_data" : o.metadata.json(),
                "speech" : o.text()
            }
        else:
            # Base class will raise the TypeError.
            return super().default(o)


class SpeechDecoder(json.JSONDecoder):
    def __init__(self, object_hook=None, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
        self.fn = kwargs.get('filename', None)
    def object_hook(self, o):
        if 'speech_data' in o:
            spd = SPData(o['speech_data']['parliament_election_year'],
                         o['speech_data']['date_of_speech'],
                         o['speech_data']['speaker_id'],
                         o['speech_data']['speaker_first_name'],
                         o['speech_data']['speaker_last_name'],
                         o['speech_data']['mp_chair'],
                         o['speech_data']['mp_deputy_chair'],
                         o['speech_data']['mp_regular'],
                         o['speech_data']['mp_governing_party'],
                         o['speech_data']['guest'],
                         o['speech_data']['government_minister'],
                         o['speech_data']['speaker_gender'],
                         o['speech_data']['speaker_birth_date'],
                         o['speech_data']['parliamentary_group'],
                         o['speech_data']['political_party'],
                         o['speech_data']['electoral_list'],
                         o['speech_data']['transcript_url'],
                         o['speech_data']['session'],
                         o['speech_data']['sitting_type'],
                         o['speech_data']['general_header'],
                         o['speech_data']['agenda_item']
                         )
            sp = o['speech']
            ssp = Speech(spd, sp)
            return ssp
        return o


## --- Functions ---
# --- Functions ---
def xmlnotes(element: etree._Element, text: str, notes: list):
    a = 0
    nl = notes.pop(0)
    element.text = text[a:nl['algus']]
    n = etree.SubElement(element, 'note')
    n.text = nl['note']
    n.tail = text[nl['ots']:]
    a = nl['ots']
    e = element
    while notes:
        nl = notes.pop(0)
        n = etree.Element('note')
        n.text = nl['note']
        n.tail = text[nl['ots']:]
        e.append(n)
        e = element
    return element

def notes_to_xml(text: str, notes: list, starttag: str, endtag: str):
    st_tag = '<note>'
    end_tag = '</note>'
    a = 0
    outtext = ''
    while notes:
        nl = notes.pop(0)
        outtext = outtext + text[a:nl['algus']] + st_tag + nl['note'] + end_tag
        a = nl['ots']
    if nl['ots'] < len(text):
        outtext = outtext + text[nl['ots']:]
    outtext = starttag + outtext + endtag
    return outtext


def make_tei_header(titles: list = [],
                    # meetings: list = [],
                    respStmt: list = [],
                    funder: list = [],
                    edition: str = None,
                    extent: list = [],
                    publisher: list = [],
                    idno: dict = {},
                    availability: str = None,
                    use_dates: bool = False,
                    publication_date: str = None,
                    bibl: str = None,
                    bibl_url: str = None,
                    project_description: str = None,
                    tagsDecl: list = [],
                    setting: str = None,
                    setting_date: str = None
                    ):
    stopwords = ['text', 'lang', 'id', 'element', 'content']
    bparser = etree.XMLParser(remove_blank_text=True)
    th = etree.Element('teiHeader')
    fd = etree.SubElement(th, 'fileDesc')
    ts = etree.SubElement(fd, 'titleStmt')
    if titles:
        for i in titles:
            e = etree.SubElement(ts, i['element'])
            e.text = i['text']
            if 'lang' in i.keys():
                e.set('{{{}}}lang'.format(XMLNS), i['lang'])
            for k in i.keys():
                if k not in stopwords:
                    e.set(k, i[k])
    rs = etree.SubElement(ts, 'respStmt')
    if respStmt:
        for i in respStmt:
            if 'name' in i.keys():
                person_name = etree.SubElement(rs, 'persName')
                person_name.text = i['name']
                if 'orcid' in i.keys():
                    if not i['orcid'].startswith('https:'):
                        i['orcid'] = 'https://orcid.org/{}'.format(i['orcid'])
                    person_name.set('ref', i['orcid'])
            if 'resp' in i.keys():
                resp = etree.SubElement(rs, 'resp')
                resp.text = i['resp']
                if 'lang' in i.keys():
                    resp.set('{{{}}}lang'.format(XMLNS), i['lang'])
    funder_e = etree.SubElement(ts, 'funder')
    if funder:
        for i in funder:
            e = etree.SubElement(funder_e, i['element'])
            e.text = i['text']
            if 'lang' in i.keys():
                e.set('{{{}}}lang'.format(XMLNS), i['lang'])
    es = etree.SubElement(fd, 'editionStmt')
    if edition:
        e_e = etree.SubElement(es, 'edition')
        e_e.text = edition
    e_extent = etree.SubElement(fd, 'extent')
    if extent:
        for i in extent:
            e = etree.SubElement(e_extent, i['element'])
            e.text = i['text']
            if 'lang' in i.keys():
                e.set('{{{}}}lang'.format(XMLNS), i['lang'])
            for k in i.keys():
                if k not in stopwords:
                    e.set(k, i[k])
    ps = etree.SubElement(fd, 'publicationStmt')
    publisher_e = etree.SubElement(ps, 'publisher')
    if publisher:
        for i in publisher:
            e = etree.SubElement(publisher_e, i['element'])
            e.text = i['text']
            if 'lang' in i.keys():
                e.set('{{{}}}lang'.format(XMLNS), i['lang'])
    idno_e = etree.SubElement(ps, 'idno')
    if idno:
        idno_e.text = idno['text']
        for i in idno.keys():
            if i != 'text':
                idno_e.set(i, idno[i])
    if availability:
        availability_e = etree.fromstring(availability, parser=bparser)
        ps.append(availability_e)
    else:
        availability_e = etree.SubElement(ps, 'availability')
    if use_dates and publication_date:
        pub_date = etree.SubElement(ps, 'date')
        pub_date.text = publication_date
        pub_date.set('when', publication_date)
    else:
        pub_date = etree.SubElement(ps, 'date')
    source_desc = etree.SubElement(fd, 'sourceDesc')
    if bibl:
        bibl_e = etree.fromstring(bibl, parser=bparser)
        source_desc.append(bibl_e)
        if bibl_url:
            bibl_u = etree.SubElement(bibl_e, 'idno')
            bibl_u.set('type', 'URI')
            bibl_u.text = bibl_url
    else:
        bibl_e = etree.SubElement(source_desc, 'bibl')
    ed = etree.SubElement(th, 'encodingDesc')
    if project_description:
        project_desc = etree.fromstring(project_description,
                                        parser=bparser)
        ed.append(project_desc)
    else:
        project_desc = etree.SubElement(ed, 'projectDesc')
    td = etree.SubElement(ed, 'tagsDecl')
    if tagsDecl:
        for i in tagsDecl:
            ns = etree.SubElement(td, i['element'])
            for k in i.keys():
                if k not in stopwords:
                    ns.set(k, i[k])
                elif k == 'content':
                    for m in i['content']:
                        tu = etree.SubElement(ns, m['element'])
                        for n in m.keys():
                            if n not  in stopwords:
                                tu.set(n, m[n])
    pd = etree.SubElement(th, 'profileDesc')
    setting_desc = etree.SubElement(pd, 'settingDesc')
    if setting:
        setting_e = etree.fromstring(setting,
                                     parser=bparser)
        setting_desc.append(setting_e)
    else:
        setting_e = etree.SubElement(setting_desc, 'setting')
    if use_dates and setting_date:
        s_date = etree.Element('date', {'when':setting_date})
        s_date.text = setting_date
        setting_e.append(s_date)
    return th

def make_tei_text(attrs: dict = {}, content: list = []):
    restricted = ['element','text']
    tt = etree.Element('text')
    if attrs:
        for i in attrs.keys():
            tt.set(i, attrs[i])
    body = etree.SubElement(tt, 'body')
    div = etree.SubElement(body, 'div', {'type': 'debateSection'})
    if content is not None:
        for i in content:
            div.append(i)
    return tt

def make_corpus_root(id: str = None, ana: str = None):
    root = etree.fromstring(
        '<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="et"/>')
    if id:
        root.set('{{{}}}id'.format(XMLNS), id)
    if ana:
        root.set('ana', ana)
    return root

def make_seg(attrs: dict = {}, content: list = []):
    seg = etree.Element('seg')
    if attrs:
        for i in attrs.keys():
            if i.startswith('xml:'):
                seg.set('{{{}}}{}'.format(XMLNS, i[4:]), attrs['id'])
            elif i == 'id':
                seg.set('{{{}}}id'.format(XMLNS), attrs['id'])
            elif i == 'lang':
                seg.set('{{{}}}lang'.format(XMLNS), attrs['lang'])
            elif not ':' in i:
                seg.set(i, attrs[i])
            else:
                pass
    if content:
        while content:
            # may be mixed content
            a = content.pop()
            if isinstance(a, str):
                seg.text = a
    return seg

def count_tags(tags: list, document: etree._Element):
    out = [
        {'element': 'namespace', 'name': "http://www.tei-c.org/ns/1.0",
         'content': [
             {'element': 'tagUsage', 'gi': 'text', 'occurs': '1'}
         ]
         }
    ]
    for i in tags:
        c = {'element': 'tagUsage',
             'gi': i,
             'occurs' : str(len(document.findall('.//{}'.format(i))))}
        out[0]['content'].append(c)
    return out


def translate_title(intext: str) -> str:
    """
    Translates intext from Estonian to English
    :param intext:
    :return:
    """
    out = intext
    pd = [('Esmaspäev', 'Monday'),
     ('Teisipäev', 'Tuesday'),
     ('Kolmapäev', 'Wensday'),
     ('Neljapäev', 'Thursday'),
     ('Reede', 'Friday'),
     ('Laupäev', 'Saturday')]
    for i in pd:
        if i[0] in out:
            out = out.replace(i[0], i[1])
    out = out.replace('Riigikogu erakorraline istungjärk', 'Extraordinary session of the Riigikogu')
    out = out.replace('Riigikogu täiendav istung', 'Additional session of the Riigikogu')
    out = out.replace('Riigikogu', 'Parliament term')
    out = out.replace('Istungjärk', 'Session')
    out = out.replace('Eesti iseseisvuse taastamise 30. aastapäevale pühendatud \
    XIV Riigikogu ja 20. Augusti Klubi pidulik istung',
                      'XIV Parlieament and August 20th Club Meeting dedicated to \
                      30th annivesary of restoration of independence')
    out = out.replace('täiskogu korraline istung', 'Plenary Assembly regular meeting on')
    out = out.replace('täiskogu istung', 'Plenary Assembly meeting on')
    out = out.replace('infotund', 'information session')
    out = out.replace('Ukraina presidendi Volodõmõr Zelenskõi videopöördumine',
                      'Video address of Ukrainian President Volodymyr Zelenskyi')
    return out

def get_date(intext: str) -> str:
    """
    Extracts date from text. Date should be in ISO format
    YYYY-MM-DD[*HH[:MM[:SS[.mmm[mmm]]]][+HH:MM[:SS[.ffffff]]]]
    :Note:
    Just now YYYY-MM-DD is implemented.
    :param intext:
    String text containing date
    :return:
    Date as YYYY-MM-DD
    """
    datepattern = re.compile(r'[12][09]\d{2}[-][0-2]\d[-][0-3]\d')
    leitu = datepattern.search(intext)
    return leitu.group(0)


def ref_or_covid(date: str):
    tocheck = datetime.datetime.fromisoformat(date)
    ref = datetime.datetime.fromisoformat(REFERENCE_DATE)
    covid = datetime.datetime.fromisoformat(COVID_DATE)
    if tocheck <= ref:
        return '#reference'
    if tocheck >= covid:
        return '#covid'
    else:
        sys.exit()

def make_meetings(year, session, date, rk_labels = rk_labels, session_labels = session_labels):
    out = []
    for i in rk_labels:
        if i['year'] == str(year):
            out.append({'corresp': '#ee_parliament',
            'ana': '#parla.uni #parla.term #{}'.format(i['id']), 'text': i['label'],
                        'element':'meeting'})
    for i in session_labels:
        try:
            if i['label'] == session:
                out.append(
                    {'corresp': '#ee_parliament',
                'ana': '#parla.uni #parla.session', 'n':i['id'], 'text':i['label'],
                     'element':'meeting'}
                     )
        except:
            print(i)
            print(session)
            sys.exit()
    out.append({'corresp': '#ee_parliament',
                    'ana': '#parla.uni #parla.sitting', 'n':date, 'text': date,
                'element':'meeting'}
               )
    return out

def wordtag(w):
    if w.xpostag == 'Z':
        return 'pc'
    return 'w'

def speaker_type(*args):
    if args[0]:
        return '#chair'
    elif args[1]:
        return '#deputy_chair'
    elif args[2]:
        return '#regular'
    elif args[3]:
        return '#governing_party'
    elif args[4]:
        return '#regular'
        # return "#government_minister"
    elif args[5]:
        return '#guest'
    return '#speaker_type'

def stanza_analysis(s):
    stanza_tagger_sent.tag(s)
    word_level_ner.tag(s)
    return s.stanza_syntax_sent

def features(f: dict):
    kvs = ['{}={}'.format(k,v) for k,v in f.items()]
    return '|'.join(kvs)

def analyse(t: Text):
    t.tag_layer(['morph_analysis', 'words', 'clauses'])
    return t

def returnparser():
    parser = argparse.ArgumentParser(
        description='ParlaMint files to TEI and other formats'
    )
    parser.add_argument('infile')
    parser.add_argument('outpath')

    parser.add_argument('-d', '--debug', action='store_true', default=False)
    parser.add_argument('-t', '--text', action='store_true', default=False)
    parser.add_argument('-c', '--conllu', action='store_true', default=False)
    parser.add_argument('-x', '--xml', action='store_true', default=False)
    parser.add_argument('-a', '--anal', action='store_true', default=False)
    parser.add_argument('-v', '--vert', action='store_true', default=False)
    parser.add_argument('-n', '--notes')
    parser.add_argument('-s', '--sample', action='store_true', default=False)
    return parser

def read_notelist(filename: str) -> list:
    with open(filename, 'r') as f:
        lines = [x.rstrip() for x in f.readlines()]
    return [x[8:] for x in lines]

def make_notes(text: str, notes: list):
    outlist = []
    def _sf(x):
        return x['algus']
    if notes is None:
        print('Nõutisid ei olegi!')# there is no note list, return with empty list
        return outlist
    for i in notes:
        algus = 0
        ots = algus + len(i) +1
        n = text.count(i)
        if n == 0:
            continue
        else:
            while n > 0:
                a = text.find(i, algus)
                ot = a + len(i)
                outlist.append({'algus': a, 'ots':ot, 'vahe': ot - a, 'note':i})
                algus = ot
                ots = algus + len(i)
                n -=1
    outlist.sort(key=_sf)
    return outlist

def txt_minus_notes(text: str, notes: list):
    a = 0
    uustekst = ''
    if not notes:
        return text
    for i in notes:
        uustekst = uustekst + text[a:i['algus']]
        a = i['ots']
    uustekst = uustekst + text[i['ots']:]
    return uustekst


## --- Main ---
def main(p: argparse.ArgumentParser):
    args = p.parse_args()
    with open(args.infile, 'rb') as infile:
        Speech.filename = infile.name
        Speech.outpath = args.outpath
        # print(os.path.join(Speech.outpath, Speech.filename))
        data = json.load(infile, cls=SpeechDecoder)
        # print(data)
    if args.notes:
        NOTELIST = read_notelist(args.notes)
    else:
        NOTELIST = None

    if args.debug:
        print(len(data))
        print(args.outpath)
        b = SPData()
        a = Speech(b)

        print('b = {}'.format(b))
        print('a = {}'.format(a))
        c = a.xml()
        print('c = {}'.format(c))
    if args.text:
        #TODO: Delete old file, if exists!
        tlist = [x.text() for x in data]
    if args.conllu:
        #TODO: Delete old file, if exists!
        olist = [x.conllu() for x in data]
    if args.xml:
        # build xml
        sampletext = ''
        xmlcontentsisu = []
        titlelist = []
        for i in data:
            if args.anal:
                xmlcontentsisu.extend(i.xml(NOTELIST, True))
            else:
                xmlcontentsisu.extend(i.xml(NOTELIST))

        if not args.anal:
            filename = data[0].fn
        else:
            filename = data[0].fn + '.ana'

        sessiondate = get_date(data[0].fn)

        # === TITLES ===
        sess = data[0].metadata.session
        d = data[0].metadata.date_of_speech.split()[0]
        y = data[0].metadata.parliament_election_year

        if args.anal:
            if args.sample:
                sampletext = " SAMPLE"
            title_text =  'Estonian parliamentary corpus ParlaMint-EE, {} [ParlaMint.ana{}]'.format(
                get_date(filename), sampletext)
        else:
            if args.sample:
                sampletext = " SAMPLE"
            title_text = 'Estonian parliamentary corpus ParlaMint-EE, {} [ParlaMint{}]'.format(
                get_date(filename), sampletext)


        titlelist.append({'element':'title', 'lang':'en', 'type': 'main', 'text':title_text})

        # --- subtitles ---
        subtitletxt = data[0].metadata.general_header
        titlelist.append({'element': 'title', 'lang': 'et', 'type': 'sub', 'text': subtitletxt})
        titlelist.append({'element': 'title', 'lang': 'en', 'type': 'sub', 'text': translate_title(subtitletxt)})

        # --- meetings ---
        meetings = make_meetings(y, sess, d)
        titlelist.extend(meetings)
        teitext = make_tei_text(attrs={'ana':ref_or_covid(sessiondate)},
                                content=xmlcontentsisu)

        no_of_speeches = len(teitext.findall('.//{}'.format('u')))
        no_of_words = len(teitext.findall('.//{}'.format('w'))) or Speech.wordCounter

        # --- count extent ---
        extent = [
            {'element': 'measure', 'unit': 'speeches',
             'quantity': '{}'.format(no_of_speeches), 'lang': 'et',
             'text': '{} kõnet'.format(no_of_speeches)},
            {'element': 'measure', 'unit': 'speeches',
             'quantity': '{}'.format(no_of_speeches), 'lang': 'en',
             'text': '{} speeches'.format(no_of_speeches)},
            {'element': 'measure', 'unit': 'words',
             'quantity': '{}'.format(no_of_words), 'lang': 'et',
             'text': '{} sõna'.format(no_of_words)},
            {'element': 'measure', 'unit': 'words',
             'quantity': '{}'.format(no_of_words), 'lang': 'en',
             'text': '{} words'.format(no_of_words)}
        ]

        # --- count elements ---
        tags_decl = count_tags(['note', 'u', 'seg'], teitext)

        # === MAKE ROOT ===
        root = make_corpus_root(id = filename,
                                ana = '#parla.sitting {}'.format(ref_or_covid(sessiondate))
                                )
        # --- tei header ---
        teiheader = make_tei_header(
            titles=titlelist,
            respStmt=RESP_LIST, funder=CLARIN_ERIC,
            edition='2.1', publisher=CLARIN_ERIC,
            idno=PUBLISHER_HANDLE,availability=CC_BY_40_XML,
            use_dates=True, publication_date='2023-02-15',
            bibl=BIBL,
            bibl_url=data[0].metadata.transcript_url,
            project_description=PROJECT_DESC,
            setting=RIIGIKOGU_SETTING, setting_date=get_date(filename),
            tagsDecl=tags_decl,
            extent=extent
            )
        root.append(teiheader)
        root.append(teitext)

        out = etree.tostring(root,
                             pretty_print=True,
                             encoding='unicode',
                             doctype=Speech.xml_doctype)
        if args.anal:
            xmlext = '.ana.xml'
        else:
            xmlext = '.xml'
        with open(os.path.join(args.outpath, data[0].fn + xmlext), 'w') as xf:
            xf.write(out)
    #TODO: if args.vert

if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)
