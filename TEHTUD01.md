# JSON faili teisendamine TEI kujule

## Failid

### Lähtefailid

Kogu andmestik on failis `data/steno_20211118.json.zip`. 

Väiksema mahuga andmestikud on järgmistes failides:

* data/out-1377-1378.json
* data/out-1391-1392.json
* data/out-1392.json
* data/out-2000-11-15-16.json
* data/out-2000-11-15.json
* data/out-2000.json

### Programmid

* tools/chunk\_json.py
* tools/json2tei.py
* tools/loe\_json.py

Programmiga `chunk_json.py` on võimalik algsest json failist väiksemaid 
juppe eraldada. Praeguse seisuga töötab kaks teineteist välistavat 
valikulist atribuuti: `-k` kuupäevajärgse ja `-j` istungjärgu (?) otsingu
jaoks.

Nii on käsureaga 

```
./chunk_json.py -k '2000-01-01 - 2000-12-31' ../data/steno_20211205.json ../data/out-2000.json
```

saadud üldisest failist `/steno_20211205.json` (mis erineb lahtipakitud jsonist vaid selle võrra, et puuduva väärtuse jaoks on `NaN` asemel kasutatud jsoni
vormingule vastavat väärtust `null`) saadud alamosa `out-2000.json`, mis sisaldab kõiki protokolle alates 1. jaanuarist 2000 kuni 31. detsembrini 2000.


## Osafailide genereerimine

Alamosade tekitamine käib programmiga `chunk_json.py`.
Kohustuslikeks atribuutideks on sisendfail ja väljundfail, 
valikulisteks teineteist välistavad `-k` (ehk ` --kuupaev`)
ja `-j` (ehk `--jrk`).


### Osafail järgu järgi

Osafaili järgu järgi võimaldab genereerida atribuut `-j` ehk 
`--jrk`. Atribuudi väärtuseks võib olla number või numbrite vahemik.

### Osafail kuupäeva(de) järgi

Osafaili kuupäeva(de) järgi võimaldab genereerida atribuut `-j` ehk
`--kuupaev`. Atribuudi väärtuseks võib olla kuupäev või kuupäevade
vahemik, kas kellaaegadega või ilma.

Kuupäevad kirjutatakse kõigepealt aasta, siis kuu, siis kuupäev, eraldajaiks
sidekriips (`-`). Aasta kirjutatakse neljakohalisena, kuu ja kuupäev kahekohalisena, s.t. vajaduse korral saab ühekohaline väärtus nulli ette. Nii näiteks 
märgitakse 17. jaanuar 2002 nii: `2002-01-17`.

Kellaajad kirjutatakse kahekohalisena tunnid, minutid ja sekundid, kahekümne nelja tunnise kella järgi, eraldajaks
koolon. Nii kirjutatakse kolmveerand viis peale lõunat kujul: `16:45:00`.

Kellaajad võib ka ära jätta, vaikimisi alguskellaaeg on `00:00:00` ja
lõpukellaaeg `23:59:59`.

Vahemik tähistatakse sidekriipsuga, mille alguses ja lõpus on tühik.


## TEI vorming

TEI vormingusse teisendab programm `json2tei.py`.
Kuigi põhimõtteliselt võiks ka kogu suure json faili läbi lasta, siis mõistlik
on alustada väiksemate failidega.

Alustuseks võtsin faili `out-1391-1392.json`. See on saadud algsest failist
nii: `./chunk_json.py -j "1391-1392" ../data/steno_20211205.json ../data/out-1391-1392.json` (valib algsest failist kõik kirjed, mille puhul `1391 ≥ jrk ≤ 1392`).

Fail `out-1391-1392-anal-tei.xml` (TEI koos analüüsiga) on saadud sellest failist järgmiselt:

```
./json2tei.py ../data/out-1391-1392.json ../data/out-1391-1392-anal-tei.xml -a
```

TEI failis kasutatakse praegu järgmisi jsoni välju:

* `esineja`
* `esineja_std`
* `sugu`
* `synnikuup`
* `tekst`

Kõik peale `tekst` välja on seotud esineja andmetega.

TEI faili juurelemendiks on `<teiCorpus/>`, iga json faili kirje kohta on `<TEI>` element. Esimene juurelemendi alamelement on `<teiHeader/>`, sinna koondatakse andmed kogu faili kohta. Praeguse seisuga on sinna koondatud kogu failis `<TEI/>` märgendite vahel toodud esinejate kohta käivad andmed (märgend `<listPerson/>` ja alammärgendid).

Praegu on iga jsoni faili kirje kohta oma `<TEI/>` märgend, mida sisustab `text/body/div/u`, `<u/>` on element, mille all on tekst lõikude ja lausetena.

# Viimased parandused

## 2023-01-31

Tehtud:
- [x] Source url õige kuupäev
- [x] meeting elemendi corresp atribuut
- [x] meeting elemendid juurfailides
- [~] Why haven't you included links to youtube with recordings?
- [x] Failide klassifikatsioon: sama info, mis `//setting/date/@ana`
- [ ] Märkused kõnede sees
- [ ] Algmärkused transkriptsiooni alguses
