# ParlaMint



## Viited

* [CLARINi link ParlaMint projektile](https://www.clarin.eu/content/parlamint-towards-comparable-parliamentary-corpora)
* [ParlaFormat Workshop](https://www.clarin.eu/event/2019/parlaformat-workshop)
* [Parla-CLARIN Githubis](https://github.com/clarin-eric/parla-clarin)
* [ParlaMint GitHubis](https://github.com/clarin-eric/ParlaMint)
* [ParlaMint Estonia Prep GitHubis](https://github.com/martinmolder/parlamint-estonia-prep)


## Skriptid

### Kuupäevade fail

Selleks, et teha faili, mis sisaldab kõiki kuupäevi, mis algses json failis on, eeldusel et kuupäev on väljal `date`:

```
cat ../data/parliamint_20220218.json |grep '"date":'|tr -s ' '|tr -d '"'|cut -d ' ' -f3|sort|uniq > kuupaevad.txt
```

Uusim tegelik:

```
cat ~/GIT/github/parlamint-estonia-prep/parlamint.json |grep '"date_of_speech":'|tr -s ' '|tr -d '"'|cut -d ' ' -f3|sort|uniq > kuupaevad-2022-11-16.txt

```

Katsetamiseks lühike kuupäevade fail:

```
cat kuupaevad.txt |head > mkp.txt
```

### Kuupäevade faili kasutamine

Skript, mis teeb suure faili päevasteks:

```
while read -r ; do KPV=$REPLY ; ./chunk_json.py -k "$KPV" "../data/parliamint_20220218.json" "../data/data-2022-02-18/ParlaMint-EE_$KPV.json" ; done < mkp.txt
```
uusim:

```
while read -r ; do KPV=$REPLY ; ./chunk_json.py -k "$KPV" "../data/steno_texts_clean_added_20220131.json" "../data/data-2022-01-31/ParlaMint-EE_$KPV.json" ; done < kuupaevad01.txt 
```


Kui sisaldab `NaN` väärtusi:

```
sed -i.back 's/NaN/null/g' parlamint.json
```

# Muu

## Aastate kaupa kopeerimine

```
for i in `ls -1 /home/nemee/GIT/parlamint/data/xml/|cut -d '-' -f2|sort|cut -d '_' -f2| uniq|tr '\n' ' '` ; do mkdir $i ; done

```


```
for i in `ls -1 /home/nemee/GIT/parlamint/data/xml/|cut -d '-' -f2|sort|cut -d '_' -f2| uniq|tr '\n' ' '` ; do cp /home/nemee/GIT/parlamint/data/ana/*$i* ParlaMint-EE.TEI.ana/$i ; done
```


## Sulgudes

### Unikaalsed väljendid sulgudes

```
cat ~/GIT/github/parlamint-estonia-prep/parlamint.json|egrep '[(]'|grep -v 'agenda_item'|sed -r 's/(^[^(]+)([(][^)]+[)])(.*$)/\2/g'|sort|uniq -c|sort -nr|egrep '^[[:space:]]+[1]{1}[[:space:]]'|wc -l
```


## Postfix

### Eemalda kahtlased märgid

```
for i in ParlaMint-EE_20*[0-9].xml; do sed -i.b01 's/\xe2\x80\x91/-/g; s/\xc2\xad//g' $i; done
```

### Eemalda tühikud `<note>` märgendi algusest

```
for i in ParlaMint-EE_20*[0-9].xml; do sed -i.bk1 's/\(<note[^>]*>\) /\1/1' $i; done
```

### `ana` failide `title` jama

```
for i in ParlaMint-EE_20*[0-9].ana.xml; do sed -i.b01 's/\(<title xml:lang="en" type="main">Estonian parliamentary corpus ParlaMint-EE, 20[0-9]\{2\}[-][0-9]\{2\}[-][0-9]\{2\}\)\(<\/title>\)/\1 \[ParlaMint.ana\]\2/g' $i ; done
```

Osadel on [ParlaMint] pealkirjas sees.

```
for i in ParlaMint-EE_20*[0-9].ana.xml; do sed -i.b02 's/\(<title xml:lang="en" type="main">Estonian parliamentary corpus ParlaMint-EE, 20[0-9]\{2\}[-][0-9]\{2\}[-][0-9]\{2\} \[ParlaMint\)\(\]<\/title>\)/\1.ana\2/g' $i ; done
```


