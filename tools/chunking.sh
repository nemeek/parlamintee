#!/bin/bash

conda activate py38


set -e

while read -r ; do KPV=$REPLY ; ./chunk_json.py -k "$KPV" /home/nemee/GIT/github/parlamint-estonia-prep/parlamint.json "../data/json-2022-11-16/ParlaMint-EE_$KPV.json" ; done < kuupaevad-2022-11-16.txt 

