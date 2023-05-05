#!/usr/bin/env python3
"""
Usage:
./parlamintee.py ../data/data-test/ParlaMint-EE_2015-01-12.json ../data/new-testdata/
./parlamintee.py -x ../data/data-test/ParlaMint-EE_2015-01-12.json ../data/data-2022-10-18/

Validate:
xmllint --noout --relaxng Schema/ParlaMint-TEI.rng ~/GIT/parlamint/data/data-2022-10-18/ParlaMint-EE_2015-01-12.xml
"""
import argparse
import os.path

from lxml import etree
from copy import deepcopy


L = '{http://www.w3.org/XML/1998/namespace}lang'
I = '{http://www.w3.org/XML/1998/namespace}id'
meetingdate = '2015-01-12'


xml_doctype = '<?xml version="1.0" encoding="UTF-8"?>'

tei_namespace = "http://www.tei-c.org/ns/1.0"
xml_namespace = ('http://www.w3.org/XML/1998/namespace')
include_namespace = "http://www.w3.org/2001/XInclude"
root = etree.Element('teiCorpus', xmlns=tei_namespace)
root.set('{{{}}}{}'.format(xml_namespace, 'id'), 'ParlaMint-EE')
root.set('{http://www.w3.org/XML/1998/namespace}lang', 'et')
# root.set('ana', '#parla.sitting #reference')
tei_header = etree.SubElement(root, 'teiHeader')
file_desc = etree.SubElement(tei_header, 'fileDesc')
title_stmt = etree.SubElement(file_desc, 'titleStmt')
title = etree.SubElement(title_stmt, 'title')
title.set(L, 'en')
title.text = 'Estonian parliamentary corpus ParlaMint-EE [ParlaMint SAMPLE]'

for i in ['XII Riigikogu', 'XIII Riigikogu', 'XIV Riigikogu']:
    m = etree.Element('meeting')
    m.set('ana', '#parla.term')
    m.text = i
    title_stmt.append(m)

resp_stmt = etree.SubElement(title_stmt, 'respStmt')
for i in ['Martin Mölder', 'Neeme Kahusk', 'Kadri Vider']:
    e = etree.Element('persName')
    e.text = i
    resp_stmt.append(e)
resp = etree.SubElement(resp_stmt, 'resp')
resp.set(L, 'en')
resp.text = 'Data retrieval and conversion to Parla-CLARIN TEI XML'

# pers_name = etree.SubElement(resp_stmt, 'persName')
title.set('type', 'main')

funder = etree.SubElement(title_stmt, 'funder')
cl = []
for i in [((L, 'et'), 'CLARIN ERIC teadustaristu'), ((L, 'en'), 'CLARIN ERIC research infrastructure')]:
    e = etree.Element('orgName')
    e.set(*i[0])
    e.text = i[-1]
    cl.append(e)

for i in cl:
    funder.append(deepcopy(i))
edition_stmt = etree.SubElement(file_desc, 'editionStmt')
edition = etree.SubElement(edition_stmt, 'edition')
edition.text = '2.1'
# encoding_desc = etree.SubElement(tei_header, 'encodingDesc')

extent = etree.SubElement(file_desc, 'extent')
measure = etree.SubElement(extent, 'measure')
measure.set('quantity', '10')
measure.set('unit', 'speeches')
measure.set(L, 'en')
measure.text = '10 speeches'
# about 3052716 words
measure = etree.SubElement(extent, 'measure')
measure.set('quantity', '3052716')
measure.set('unit', 'words')
measure.set(L, 'en')
measure.text = '3052716 words'
publication_stmt = etree.SubElement(file_desc, 'publicationStmt')
publisher = etree.SubElement(publication_stmt, 'publisher')
for i in cl:
    publisher.append(i)
idno = etree.SubElement(publication_stmt, 'idno')
idno.set('subtype', 'handle')
idno.set('type', 'URI')
idno.text = 'http://hdl.handle.net/11356/1431'
avail = etree.SubElement(publication_stmt, 'availability')
avail.set('status', 'free')
licence = etree.SubElement(avail, 'licence')
licence.text = 'http://creativecommons.org/licenses/by/4.0/'
p = etree.SubElement(avail, 'p')
p.set(L, 'en')
p.text = 'This work is licensed under the '
ref = etree.SubElement(p, 'ref')
ref.set('target', "http://creativecommons.org/licenses/by/4.0/")
ref.text = 'Creative Commons Attribution 4.0 International License'
ref.tail = '.'
date = etree.SubElement(publication_stmt, 'date')
date.set('when', "2021-06-10")
date.text = "2021-06-10"
source_desc = etree.SubElement(file_desc, 'sourceDesc')
bibl = etree.SubElement(source_desc, 'bibl')
bibtitle = etree.SubElement(bibl, 'title')
bibtitle.set('type', 'main')
bibtitle.set(L, 'et')
bibtitle.text = 'Riigikogu stenogrammid'
idno = etree.SubElement(bibl, 'idno')
idno.set('type', 'URI')
idno.text = 'https://stenogrammid.riigikogu.ee'

encoding_desc = etree.SubElement(tei_header, 'encodingDesc')
project_desc = etree.SubElement(encoding_desc, 'projectDesc')
p = etree.SubElement(project_desc, 'p')
p.set(L, 'en')
ref = etree.SubElement(p, 'ref')
ref.set('target', "https://www.clarin.eu/content/parlamint")
ref.text = 'ParlaMint'

# editorial_decl = etree.SubElement(encoding_desc, 'editorialDecl')
editorial_decl = etree.fromstring('''<editorialDecl>
            <correction>
               <p xml:lang="en">No correction of source texts was performed.</p>
            </correction>
            <normalization>
               <p xml:lang="en">Text has not been normalised, except for spacing.</p>
            </normalization>
            <hyphenation>
               <p xml:lang="en">No end-of-line hyphens were present in the source.</p>
            </hyphenation>
            <quotation>
               <p xml:lang="en">Quotation marks have been left in the text and are not explicitly marked up.</p>
            </quotation>
            <segmentation>
               <p xml:lang="en">The texts are segmented into utterances (speeches) and segments (corresponding to paragraphs in the source transcription).</p>
            </segmentation>
         </editorialDecl>''')
encoding_desc.append(editorial_decl)
# profile_desc = etree.SubElement(tei_header, 'profileDesc')

tags_decl = etree.SubElement(encoding_desc, 'tagsDecl')
namespace = etree.SubElement(tags_decl, 'namespace')
namespace.set('name', tei_namespace)

# TODO: real tag usage
tu = etree.SubElement(namespace, 'tagUsage')
tu.set('gi', 'text')
tu.set('occurs', '1')

profile_desc = etree.SubElement(tei_header, 'profileDesc')

setting_desc = etree.SubElement(profile_desc, 'settingDesc')
setting = etree.SubElement(setting_desc, 'setting')


name = etree.SubElement(setting, 'name')
name.set('type', 'city')
name.text = 'Tallinn'
name = etree.SubElement(setting, 'name')
name.set('type', 'country')
name.set('key', 'EE')
name.text = 'Estonia'
date = etree.SubElement(setting, 'date')

# TODO: ana not needed here, but from and to dates are. See documentation.
date.set('ana','#parla.meeting')
date.set('when', meetingdate)
date.text = meetingdate

class_decl = etree.Element('classDecl')
encoding_desc.append(class_decl)
taxonomy = etree.SubElement(class_decl, 'taxonomy')
taxonomy.set(I, 'subcorpus')
for i in [(L, 'et', 'Allkorpused'),
          (L, 'en', 'Subcorpora')]:
    desc = etree.SubElement(taxonomy, 'desc')
    desc.set(i[0], i[1])
    term = etree.SubElement(desc, 'term')
    term.text = i[2]
legis = etree.fromstring('''<xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="ParlaMint-taxonomy-parla.legislature.xml"/>''')
speakers = etree.fromstring('''<xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="ParlaMint-taxonomy-speaker_types.xml"/>''')
class_decl.append(legis)
class_decl.append(speakers)

rmsparser = etree.XMLParser(remove_blank_text=True)

kategooriad = ['''<category xml:id="reference">
   <catDesc xml:lang="et">
    <term>Referents</term>: referentskorpus, kuni 2019-10-31</catDesc>
   <catDesc xml:lang="en">
    <term>Reference</term>: reference subcorpus, until 2019-10-31</catDesc>
  </category>''',
               '''<category xml:id="covid">
   <catDesc xml:lang="et">
    <term>COVID</term>: COVIDi allkorpus, alates 2019-11-01</catDesc>
   <catDesc xml:lang="en">
    <term>COVID</term>: COVID subcorpus, from 2019-11-01 onwards</catDesc>
  </category>''']

for i in kategooriad:
    category = etree.fromstring(i, parser=rmsparser)
    taxonomy.append(category)

partic_desc = etree.fromstring('''<particDesc><xi:include xmlns:xi="http://www.w3.org/2001/XInclude"
 href="ParlaMint-EE-listOrg.xml"/><xi:include xmlns:xi="http://www.w3.org/2001/XInclude"
 href="ParlaMint-EE-listPerson.xml"/></particDesc>''')

profile_desc.append(partic_desc)

# partic_desc = etree.SubElement(profile_desc, 'particDesc')
# list_org = etree.SubElement(partic_desc, 'listOrg')
# org = etree.SubElement(list_org, 'org')
# org.set('role', 'government')
# org_name = etree.SubElement(org, 'orgName')
# org_name.set(L, 'en')
# org_name.set('full', 'yes')
# org_name.text = 'Estonian Government'
#
# list_person = etree.SubElement(partic_desc, 'listPerson')
# person = etree.SubElement(list_person, 'person')
# pers_name = etree.SubElement(person, 'persName')
# surname = etree.SubElement(pers_name, 'surname')
# surname.text = 'Nestor'
# forename = etree.SubElement(pers_name, 'forename')
# forename.text = 'Erki'

lang_usage = etree.Element('langUsage')
profile_desc.append(lang_usage)
for i in [('ident', 'et', L, 'et', 'eesti'),
          ('ident', 'en', L, 'et', 'inglise'),
          ('ident', 'et', L, 'en', 'Estonian'),
          ('ident', 'en', L, 'en', 'English')]:
    language = etree.SubElement(lang_usage, 'language', {i[0]: i[1], i[2]: i[3]})
    language.text = i[-1]


# """<xi: include
# xmlns: xi = "http://www.w3.org/2001/XInclude"
# href = "ParlaMint-LV_PT12-2014-11-05-265.xml" />"""
xi = etree.SubElement(root, '{{{}}}{}'.format(include_namespace, 'include'), nsmap={'xi':include_namespace})
xi.set('href', 'ParlaMint-EE_2015-01-12.xml')
xi = etree.SubElement(root, '{{{}}}{}'.format(include_namespace, 'include'), nsmap={'xi':include_namespace})
xi.set('href', 'ParlaMint-EE_2022-01-13.xml')


def returnparser():
    parser = argparse.ArgumentParser(
        description='ParlaMint files to TEI (teiCorpus)'
    )
    parser.add_argument('outpath')
    parser.add_argument('-f', '--fn', default='ParlaMint-EE')
    return parser

def main(p: argparse.ArgumentParser):
    args = p.parse_args()
    xmlext = '.xml'
    out = etree.tostring(root, pretty_print=True, encoding='unicode', doctype=xml_doctype)
    with open(os.path.join(args.outpath, args.fn + xmlext), 'w') as xf:
        xf.write(out)


if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)
