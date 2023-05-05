import sys
import os.path

from lxml import etree as et
from xmldiff import main, formatting
f = formatting.XmlDiffFormatter(normalize=formatting.WS_BOTH)

sys.path.insert(0, os.path.abspath('tools'))
from parlamintee import make_corpus_root, make_tei_header, make_tei_text
import parlamintee
from xmldata import BARE_TEI_HEADER, MINIMAL_TEI_HEADER, MAXIMAL_TEI_HEADER, MIN_TEI_TEXT,\
    MAXIMAL_TITLES_TEI_HEADER

lihttei = '<TEI />'
xmlnsiga ='<TEI xmlns="http://www.tei-c.org/ns/1.0"  xml:lang="et" />'
ROOTONLY = et.fromstring(xmlnsiga)

teiheader_titles = [
    {'element': 'title', 'lang': "en", 'type':"main",
     'text' : 'Estonian parliamentary corpus ParlaMint-EE, 2015-01-12 [ParlaMint SAMPLE]'},
    {'element': 'title', 'lang':"en", 'type':"sub",
     'text': 'XII Parliament term, IX Session, Plenary Assembly regular meeting on Monday, 12.01.2015, 15:00'},
    {'element':'title', 'lang':"et", 'type':"sub",
     'text':'XII Riigikogu, IX Istungjärk, täiskogu korraline istung Esmaspäev, 12.01.2015, 15:00'},
     {'element':'meeting', 'corresp':"#ee_parliament", 'ana':"#parla.uni #parla.sitting",
      'n':"2015-01-12", 'text':'2015-01-12'},
     {'element':'meeting', 'corresp':"#ee_parliament", 'ana':"#parla.uni #parla.session",
      'n':"rs9", 'text':'IX regular session'},
    {'element':'meeting', 'corresp':"#ee_parliament",
     'ana':"#parla.uni #parla.term #parliament.RK12",
     'text':'XII Riigikogu'}
]

tags_data = [
    {'element': 'namespace', 'name': "http://www.tei-c.org/ns/1.0",
     'content': [
         {'element': 'tagUsage', 'gi': 'text', 'occurs': '1'},
         {'element': 'tagUsage', 'gi': 'u', 'occurs': '42'}]
     }
    ]

def test_strings():
    assert main.diff_texts(et.tostring(make_corpus_root(), encoding='unicode'),
                           xmlnsiga) == []

def test_tei_header():
    assert main.diff_texts(et.tostring(make_tei_header(), encoding='unicode'),
                           BARE_TEI_HEADER) == []
def test_tei_min_header():
    assert main.diff_texts(et.tostring(make_tei_header(respStmt = parlamintee.RESP_LIST,
                               funder = parlamintee.CLARIN_ERIC),
                                       encoding='unicode'),
                           MINIMAL_TEI_HEADER) == []

def test_maximal_tei_header():
    assert main.diff_texts(
        et.tostring(make_tei_header(
            respStmt = parlamintee.RESP_LIST,
            funder = parlamintee.CLARIN_ERIC,
            publisher=parlamintee.CLARIN_ERIC,
            idno=parlamintee.PUBLISHER_HANDLE,
            availability=parlamintee.CC_BY_40_XML,
            use_dates=True,
            publication_date='2023-02-06',
            bibl=parlamintee.BIBL,
            bibl_url='https://stenogrammid.riigikogu.ee/et/201104041500',
            project_description=parlamintee.PROJECT_DESC,
            setting=parlamintee.RIIGIKOGU_SETTING,
            setting_date='2023-02-06'
            ),
            encoding='unicode'),
                           MAXIMAL_TEI_HEADER) == []

def test_min_tei_text():
    assert main.diff_texts(et.tostring(
        make_tei_text(content = et.Element('div',
                                           {'type':'debateSection'})),
        encoding='unicode'),
                           MIN_TEI_TEXT) == []

def test_titles_tei_header():
    assert main.diff_texts(
        et.tostring(make_tei_header(
            titles = teiheader_titles,
            respStmt = parlamintee.RESP_LIST,
            funder = parlamintee.CLARIN_ERIC,
            publisher=parlamintee.CLARIN_ERIC,
            idno=parlamintee.PUBLISHER_HANDLE,
            availability=parlamintee.CC_BY_40_XML,
            use_dates=True,
            publication_date='2023-02-06',
            bibl=parlamintee.BIBL,
            bibl_url='https://stenogrammid.riigikogu.ee/et/201104041500',
            project_description=parlamintee.PROJECT_DESC,
            setting=parlamintee.RIIGIKOGU_SETTING,
            tagsDecl = tags_data,
            setting_date='2023-02-06'
            ),
            encoding='unicode'),
                           MAXIMAL_TITLES_TEI_HEADER) == []
