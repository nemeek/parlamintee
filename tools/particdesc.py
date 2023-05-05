#!/usr/bin/env python3
"""
Usage:
./particdesc.py ~/GIT/github/parlamint-estonia-prep/mp_data.json

"""
import argparse
import datetime
import json
import os.path
import sys
import re
from copy import deepcopy

from lxml import etree
from teicorpus import L

## --- Global variables and settings ---
persons_filename = 'ParlaMint-EE-listPerson.xml'
orgs_filename = 'ParlaMint-EE-listOrg.xml'
persons_head = etree.fromstring(b'''<?xml version="1.0" encoding="UTF-8"?>
<listPerson xmlns="http://www.tei-c.org/ns/1.0"
            xml:id="ParlaMint-EE-listPerson"
            xml:lang="et" />''')
orgs_head = etree.fromstring(b'''<?xml version="1.0" encoding="UTF-8"?>
<listOrg xmlns="http://www.tei-c.org/ns/1.0"
         xml:id="ParlaMint-EE-listOrg"
         xml:lang="et" />''')

## --- Classes ---
class Person():
    def __init__(self, **kwargs):
        self.id = ""
        self.first_name = ""
        self.last_name = ""
        self.date_of_birth = ""
        self.gender = ""
        self.parl_group = []
        self.__dict__.update(**kwargs)

    def json(self):
        v = vars(self)
        return v

    def xml(self):
        root = etree.fromstring('<person xml:id="{}" />'.format(self.id))
        if type(self.list_of_names) != type([]):
            persName = etree.SubElement(root, 'persName')
            surname = etree.SubElement(persName, 'surname')
            surname.text = self.last_name
            forename = etree.SubElement(persName, 'forename')
            forename.text = self.first_name
        else:
            for names in self.list_of_names:
                fn, sn = names['name'].split()
                persName = etree.SubElement(root, 'persName')
                if 'start' in names:
                    persName.set('from', names['start'])
                if 'end' in names:
                    persName.set('to', names['end'])
                surname = etree.SubElement(persName, 'surname')
                surname.text = sn
                forename = etree.SubElement(persName, 'forename')
                forename.text = fn
        sex = etree.SubElement(root, 'sex')
        sex.set('value', translate_sex(self.gender))
        birth = etree.SubElement(root, 'birth')
        birth.set('when', self.date_of_birth)
        for i in self.parl_group:
            if not i.parl_group_id.startswith('no'):
                af = etree.SubElement(root, 'affiliation')
                af.set('ref', '#group.{}'.format(i.parl_group_id))
                af.set('role', 'member')
                af.set('from', i.start)
                af.set('to', i.end)
                for k in [('et', 'Liige'), ('en', 'Member')]:
                    rn = etree.SubElement(af, 'roleName')
                    rn.set(L, k[0])
                    rn.text = k[1]
            af = etree.SubElement(root, 'affiliation')
            af.set('ref', '#{}'.format('ee_parliament'))
            af.set('role', 'member')
            af.set('from', i.start)
            af.set('to', i.end)
            for k in [('et', 'Liige'), ('en', 'Member')]:
                rn = etree.SubElement(af, 'roleName')
                rn.set(L, k[0])
                rn.text = k[1]
        return root


class ParlGroup():
    def __init__(self, **kwargs):
        self.parl_group_name = ""
        self.parl_group_short = ""
        self.parl_group_id = ""
        self.start = ""
        self.end = ""
        self.party_membership = []

        self.__dict__.update(**kwargs)
        # self.party_membership = [type(x) for x in self.party_membership]


    def json(self):
        v = vars(self)
        return v

    def __repr__(self):
        return str(self.json())


class PartyMembership():
    def __init__(self, **kwargs):
        # self.party = ""
        # self.start = ""
        # self.end = ""
        self.__dict__.update(**kwargs)
        # self.__dict__ = {k:v for (k,v) in zip(vars(self), args)}

    def json(self):
        v = vars(self)
        return v


## --- Functions ---
def translate_sex(istr: str):
    if istr == "man":
        return "M"
    elif istr == "woman":
        return "F"
    else:
        raise Exception

def read_data(rida: dict):
    grupiliikmed = []
    otse_personisse = {x: rida[x] for x in rida if x not in ['parl_group']}
    p = Person(**otse_personisse)
    parl_group = rida['parl_group']
    for i in parl_group:
        liikmed = []
        parlamendigruppi = {y: i[y] for y in i if y not in ['party_membership']}
        pg = ParlGroup(**parlamendigruppi)
        party_membership = i['party_membership']
        for k in party_membership:
            try:
                parteiliige = PartyMembership(**k)
                liikmed.append(parteiliige)
            except TypeError:
                parteiliige = PartyMembership(partei=k)
                liikmed.append(parteiliige)
                # print(rida)
                #sys.exit()
        pg.party_membership = liikmed
        grupiliikmed.append(pg)
    p.parl_group = grupiliikmed
    return p

def parliamentary_groups(ilist: list, xml=False):
    out = []
    pgs = [x.parl_group for x in ilist]
    for i in pgs:
        for k in i:
            print(k)
            try:
                tpl = (k.parl_group_name, k.parl_group_short, k.parl_group_id)
            except:
                print(type(k))
                print(k)
            if tpl not in out and tpl[0] not in ['no group membership']:
                out.append(tpl)
            else:
                pass
    if xml:
        outxml = []
        for i in out:
            root = etree.fromstring('<org  role="parliamentaryGroup"  xml:id="group.{}" />'.format(i[2]))
            fullorgname = etree.fromstring('<orgName full="yes" xml:lang="et">{}</orgName>'.format(i[0]))
            abborgname = etree.fromstring('<orgName full="abb" >{}</orgName>'.format(i[1]))
            root.append(fullorgname)
            root.append(abborgname)
            outxml.append(root)
        return outxml
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



def returnparser():
    parser = argparse.ArgumentParser(
        description='ParlaMint files to TEI and other formats'
    )
    parser.add_argument('infile')
    # parser.add_argument('outpath')

    return parser


## --- Main ---
def main(p: argparse.ArgumentParser):
    args = p.parse_args()
    with open(args.infile, 'rb') as infile:
        data = json.load(infile)
        print(len(data))
        persons = [read_data(x) for x in data]
        print(len(persons))
        persons_xml_list = [x.xml() for x in persons]
        for i in persons_xml_list:
            persons_head.append(i)
        with open(persons_filename, 'w') as f:
            f.write(etree.tostring(persons_head, encoding='unicode', pretty_print=True))
        pgs = parliamentary_groups(persons, True)
        print(len(pgs))
        print(pgs)
        # for i in pgs:
        #     orgs_head.append(i)
        # with open(orgs_filename, 'w') as f:
        #     f.write(etree.tostring(orgs_head, encoding="unicode", pretty_print=True))




if __name__ == '__main__':
    argparser = returnparser()
    main(argparser)
