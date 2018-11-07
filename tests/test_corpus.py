#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
from momblish.corpus import Corpus
from momblish.corpus_analyzer import CorpusAnalyzer

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


class TestCorpus(object):
    """Corpus's can save and load themselves from json"""

    def test_load(self, corpus):
        """Saves the corpus to a json file"""
        corpus.save('/tmp/corpus.json')
        assert os.path.exists('/tmp/corpus.json')

    def test_grouped_trigrams(self, corpus):
        """Loads an existing corpus from a JSON file"""

        corpus.save('/tmp/corpus2.json')
        new_corpus = Corpus.load('/tmp/corpus2.json')

        assert corpus == new_corpus
