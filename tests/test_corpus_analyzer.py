#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
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
def corpus_analyzer():
    return CorpusAnalyzer(test_corpus)


class TestCorpusAnalyzer(object):
    """Corpus Analyzes an interable to provide generation rules"""

    def test_weighted_bigrams(self, corpus_analyzer):
        """ Initializes common starting bigrams for words in the corpus"""
        weighted_bigrams_expected = {
               'AB': 0.08333333333333333,
               'AC': 0.08333333333333333,
               'AD': 0.08333333333333333,
               'BA': 0.08333333333333333,
               'BC': 0.08333333333333333,
               'BD': 0.08333333333333333,
               'CA': 0.08333333333333333,
               'CB': 0.08333333333333333,
               'CD': 0.08333333333333333,
               'DA': 0.08333333333333333,
               'DB': 0.08333333333333333,
               'DC': 0.08333333333333333
        }

        assert corpus_analyzer.corpus.weighted_bigrams == weighted_bigrams_expected

    def test_grouped_trigrams(self, corpus_analyzer):
        """ Initializes all trigrams, and groups them by preceding bigrams"""

        occurrences_expected = {
             'AB': {'C': 0.5, 'D': 0.5},
             'AC': {'B': 0.5, 'D': 0.5},
             'AD': {'B': 0.5, 'C': 0.5},
             'BA': {'C': 0.5, 'D': 0.5},
             'BC': {'A': 0.5, 'D': 0.5},
             'BD': {'A': 0.5, 'C': 0.5},
             'CA': {'B': 0.5, 'D': 0.5},
             'CB': {'A': 0.5, 'D': 0.5},
             'CD': {'A': 0.5, 'B': 0.5},
             'DA': {'B': 0.5, 'C': 0.5},
             'DB': {'A': 0.5, 'C': 0.5},
             'DC': {'A': 0.5, 'B': 0.5},
        }

        assert corpus_analyzer.corpus.occurrences == occurrences_expected

    def test_trigrams_exclude_punctuation(self):
        bad_corpus = [
             'ecdf',
             'ec\n',
             'ec!f',
        ]

        expected = {
              'EC': {'D': 1.0},
              'CD': {'F': 1.0}
        }

        c = CorpusAnalyzer(corpus=bad_corpus)

        assert c.corpus.occurrences == expected
