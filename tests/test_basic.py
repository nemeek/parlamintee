"""
https://www.tutorialspoint.com/pytest/pytest_quick_guide.htm
https://www.nerdwallet.com/blog/engineering/5-pytest-best-practices/
"""
import sys
import os.path

sys.path.insert(0, os.path.abspath('tools'))
print(sys.path)

from parlamintee import read_notelist, make_notes, txt_minus_notes
from xmldata import NOTEDE_VASTUS, NOTEDEGA_TEKST, NOTEDETA_TEKST

notefilespath = 'tests/data/minimal_notesfile.txt'
print(os.path.abspath(notefilespath))

NOTE_VASTUS = [
    '(Kaugühendus)',
    '(Juhataja helistab kella.)',
    '(Aplaus.)',
    '(Naer saalis.)',
    '(Hääl saalist.)',
    '(Naerab.)',
    '(Naer.)'
]

# test tests
def test_greater():
   num = 101
   assert num > 100

# notelist
def test_notelist_reader():
    vastus = read_notelist(notefilespath)
    assert vastus == NOTE_VASTUS

def test_simple_notes():
    vastus = make_notes(NOTEDEGA_TEKST, NOTE_VASTUS)
    assert vastus == NOTEDE_VASTUS

def test_minus_notes():
    vastus = txt_minus_notes(NOTEDEGA_TEKST, NOTEDE_VASTUS)
    assert vastus == NOTEDETA_TEKST
