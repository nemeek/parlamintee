SIMPLE_ROOT = """<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="et"> 
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <respStmt/>
        <funder/>
      </titleStmt>
      <editionStmt/>
      <extent/>
      <publicationStmt>
        <publisher/>
        <idno/>
        <availability/>
        <date/>
      </publicationStmt>
      <sourceDesc>
        <bibl/>
      </sourceDesc>
    </fileDesc>
    <encodingDesc>
      <projectDesc/>
      <tagsDecl/>
    </encodingDesc>
    <profileDesc>
      <settingDesc>
        <setting/>
      </settingDesc>
    </profileDesc>
  </teiHeader>
</TEI>
"""

BARE_TEI_HEADER = """
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <respStmt/>
        <funder/>
      </titleStmt>
      <editionStmt/>
      <extent/>
      <publicationStmt>
        <publisher/>
        <idno/>
        <availability/>
        <date/>
      </publicationStmt>
      <sourceDesc>
        <bibl/>
      </sourceDesc>
    </fileDesc>
    <encodingDesc>
      <projectDesc/>
      <tagsDecl/>
    </encodingDesc>
    <profileDesc>
      <settingDesc>
        <setting/>
      </settingDesc>
    </profileDesc>
  </teiHeader>
"""

MINIMAL_TEI_HEADER = """
<teiHeader>
  <fileDesc>
    <titleStmt>
      <respStmt>
        <persName ref="https://orcid.org/0000-0002-9701-1771">Martin Mölder</persName>
        <persName ref="https://orcid.org/0000-0003-0511-5854">Neeme Kahusk</persName>
        <persName ref="https://orcid.org/0000-0003-0966-8341">Kadri Vider</persName>
        <resp xml:lang="en">Data retrieval and conversion to Parla-CLARIN TEI XML</resp>
      </respStmt>
      <funder>
        <orgName xml:lang="et">CLARIN ERIC teadustaristu</orgName>
        <orgName xml:lang="en">CLARIN ERIC research infrastructure</orgName>
      </funder>
    </titleStmt>
    <editionStmt/>
    <extent/>
    <publicationStmt>
      <publisher/>
      <idno/>
      <availability/>
      <date/>
    </publicationStmt>
    <sourceDesc>
      <bibl/>
    </sourceDesc>
  </fileDesc>
  <encodingDesc>
    <projectDesc/>
    <tagsDecl/>
  </encodingDesc>
  <profileDesc>
    <settingDesc>
      <setting/>
    </settingDesc>
  </profileDesc>
</teiHeader>
"""

MAXIMAL_TEI_HEADER = """
<teiHeader>
  <fileDesc>
    <titleStmt>
      <respStmt>
        <persName ref="https://orcid.org/0000-0002-9701-1771">Martin Mölder</persName>
        <persName ref="https://orcid.org/0000-0003-0511-5854">Neeme Kahusk</persName>
        <persName ref="https://orcid.org/0000-0003-0966-8341">Kadri Vider</persName>
        <resp xml:lang="en">Data retrieval and conversion to Parla-CLARIN TEI XML</resp>
      </respStmt>
      <funder>
        <orgName xml:lang="et">CLARIN ERIC teadustaristu</orgName>
        <orgName xml:lang="en">CLARIN ERIC research infrastructure</orgName>
      </funder>
    </titleStmt>
    <editionStmt/>
    <extent/>
    <publicationStmt>
      <publisher>
        <orgName xml:lang="et">CLARIN ERIC teadustaristu</orgName>
        <orgName xml:lang="en">CLARIN ERIC research infrastructure</orgName>
      </publisher>
      <idno subtype="handle" type="URI">http://hdl.handle.net/11356/1431</idno>
      <availability status="free">
        <licence>http://creativecommons.org/licenses/by/4.0/</licence>
        <p xml:lang="en">This work is licensed under the <ref target="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</ref>.</p>
      </availability>
      <date when="2023-02-06">2023-02-06</date>
    </publicationStmt>
    <sourceDesc>
      <bibl>
        <title type="main" xml:lang="et">Riigikogu stenogrammid</title>
        <idno type="URI">https://stenogrammid.riigikogu.ee/et/201104041500</idno>
      </bibl>
    </sourceDesc>
  </fileDesc>
  <encodingDesc>
    <projectDesc>
      <p xml:lang="en">
        <ref target="https://www.clarin.eu/content/parlamint">ParlaMint</ref>
      </p>
    </projectDesc>
    <tagsDecl/>
  </encodingDesc>
  <profileDesc>
    <settingDesc>
      <setting>
        <name type="org">Riigikogu</name>
        <name type="address">Lossi plats 1a</name>
        <name type="city">Tallinn</name>
        <name type="country" key="EE">Estonia</name>
        <date when="2023-02-06">2023-02-06</date>
      </setting>
    </settingDesc>
  </profileDesc>
</teiHeader>"""

MIN_TEI_TEXT = """
<text>
  <body>
    <div type="debateSection"/>
  </body>
</text>
"""

NOTEDEGA_TEKST = """Palju õnne! (Aplaus.) Nüüd (Aplaus.) on juhataja väikese dilemma ees: 
saalist kostusid mitmed hõiked, et võiks juhataja vaheaja võtta, 
siis saaks Markole õnne soovida.(Juhataja helistab kella.)"""

NOTEDE_VASTUS = [{'algus': 12, 'ots': 21, 'vahe': 9, 'note': '(Aplaus.)'},
                 {'algus': 27, 'ots': 36, 'vahe': 9, 'note': '(Aplaus.)'},
                 {'algus': 169, 'ots': 195, 'vahe': 26, 'note': '(Juhataja helistab kella.)'}]

NOTEDETA_TEKST = """Palju õnne!  Nüüd  on juhataja väikese dilemma ees: 
saalist kostusid mitmed hõiked, et võiks juhataja vaheaja võtta, 
siis saaks Markole õnne soovida."""

MAXIMAL_TITLES_TEI_HEADER = """
<teiHeader>
  <fileDesc>
    <titleStmt>
        <title xml:lang="en" type="main">Estonian parliamentary corpus ParlaMint-EE, 2015-01-12 [ParlaMint SAMPLE]</title>
        <title xml:lang="en" type="sub">XII Parliament term, IX Session, Plenary Assembly regular meeting on Monday, 12.01.2015, 15:00</title>
        <title xml:lang="et" type="sub">XII Riigikogu, IX Istungjärk, täiskogu korraline istung Esmaspäev, 12.01.2015, 15:00</title>
        <meeting corresp="#ee_parliament" ana="#parla.uni #parla.sitting" n="2015-01-12">2015-01-12</meeting>
        <meeting corresp="#ee_parliament" ana="#parla.uni #parla.session" n="rs9">IX regular session</meeting>
        <meeting corresp="#ee_parliament" ana="#parla.uni #parla.term #parliament.RK12">XII Riigikogu</meeting>
      <respStmt>
        <persName ref="https://orcid.org/0000-0002-9701-1771">Martin Mölder</persName>
        <persName ref="https://orcid.org/0000-0003-0511-5854">Neeme Kahusk</persName>
        <persName ref="https://orcid.org/0000-0003-0966-8341">Kadri Vider</persName>
        <resp xml:lang="en">Data retrieval and conversion to Parla-CLARIN TEI XML</resp>
      </respStmt>
      <funder>
        <orgName xml:lang="et">CLARIN ERIC teadustaristu</orgName>
        <orgName xml:lang="en">CLARIN ERIC research infrastructure</orgName>
      </funder>
    </titleStmt>
    <editionStmt/>
    <extent/>
    <publicationStmt>
      <publisher>
        <orgName xml:lang="et">CLARIN ERIC teadustaristu</orgName>
        <orgName xml:lang="en">CLARIN ERIC research infrastructure</orgName>
      </publisher>
      <idno subtype="handle" type="URI">http://hdl.handle.net/11356/1431</idno>
      <availability status="free">
        <licence>http://creativecommons.org/licenses/by/4.0/</licence>
        <p xml:lang="en">This work is licensed under the <ref target="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</ref>.</p>
      </availability>
      <date when="2023-02-06">2023-02-06</date>
    </publicationStmt>
    <sourceDesc>
      <bibl>
        <title type="main" xml:lang="et">Riigikogu stenogrammid</title>
        <idno type="URI">https://stenogrammid.riigikogu.ee/et/201104041500</idno>
      </bibl>
    </sourceDesc>
  </fileDesc>
  <encodingDesc>
    <projectDesc>
      <p xml:lang="en">
        <ref target="https://www.clarin.eu/content/parlamint">ParlaMint</ref>
      </p>
    </projectDesc>
    <tagsDecl>
      <namespace name="http://www.tei-c.org/ns/1.0">
        <tagUsage gi="text" occurs="1"/>
        <tagUsage gi="u" occurs="42"/>
      </namespace>
    </tagsDecl>
  </encodingDesc>
  <profileDesc>
    <settingDesc>
      <setting>
        <name type="org">Riigikogu</name>
        <name type="address">Lossi plats 1a</name>
        <name type="city">Tallinn</name>
        <name type="country" key="EE">Estonia</name>
        <date when="2023-02-06">2023-02-06</date>
      </setting>
    </settingDesc>
  </profileDesc>
</teiHeader>"""
