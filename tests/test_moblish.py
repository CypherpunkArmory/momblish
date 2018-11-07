#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import random
from momblish.corpus_analyzer import CorpusAnalyzer
from momblish import Momblish

__author__ = "Stephen Prater"
__copyright__ = "Stephen Prater"
__license__ = "mit"

test_corpus = [
   'abcd',
   'abdc',
   'acbd',
   'acdb',
   'adbc',
   'adcb',
   'bacd',
   'badc',
   'bcad',
   'bcda',
   'bdac',
   'bdca',
   'cabd',
   'cadb',
   'cbad',
   'cbda',
   'cdab',
   'cdba',
   'dabc',
   'dacb',
   'dbac',
   'dbca',
   'dcab',
   'dcba'
]


@pytest.fixture
def corpus():
    return CorpusAnalyzer(test_corpus).corpus


@pytest.fixture
def momblish(corpus):
    return Momblish(corpus)


class TestMomblish(object):
    """Can generate random words from a corpus"""

    def test_words(self, momblish):
        """Generates a single word"""

        # Because the test corpus is the permutation of `abcd` we know that
        # only the letters 'abcd' can be included in generated words
        # we seed the random number generator here to make sure we get what
        # we expect out of it
        random.seed(10)
        word = momblish.word(10).lower()
        assert word == 'cadcbadcba'

    def test_sentence(self, momblish):
        """Generates N words of random length as an iterator"""

        random.seed(10)
        title = [word.lower() for word in momblish.sentence(4, word_length=4)]
        assert title == ['cadc', 'adca', 'cbda', 'bacd']

    def test_infinit_sentence(self, momblish):
        """Generates any number words of random length as a generator"""

        random.seed(10)
        w = momblish.sentence()
        assert next(w) == 'ABCDBCDA'
        assert next(w) == 'CADB'

    def test_loads_english_dictionary(self):
        """Loads the english dictionary from /usr/share/dict or /usr/share/dict/web2"""

        m = Momblish.english()
        assert m.corpus.occurences
