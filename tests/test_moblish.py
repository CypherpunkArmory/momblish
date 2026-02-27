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

    def test_words_with_prefix(self, momblish):
        """Generates a single word that starts with the supplied prefix"""

        random.seed(10)
        word = momblish.word(6, prefix='d')
        assert word == 'DBCADC'

    def test_words_with_multi_bigram_prefix(self, momblish):
        """Generates a single word that preserves a longer prefix"""

        random.seed(10)
        word = momblish.word(7, prefix='dabc')
        assert word == 'DABCADC'

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
        assert m.corpus.occurrences

    def test_caches_english_corpus_in_xdg_cache(self, monkeypatch, tmp_path):
        """Caches the analyzed english corpus in the XDG cache directory"""

        dict_file = tmp_path / 'words'
        dict_file.write_text('\n'.join(test_corpus))
        monkeypatch.setattr('momblish.momblish.lookup_dict', lambda lang: str(dict_file))
        monkeypatch.setenv('XDG_CACHE_HOME', str(tmp_path / 'cache'))

        first = Momblish.english()

        cache_file = tmp_path / 'cache' / 'momblish' / 'english.json'
        assert cache_file.exists()

        dict_file.write_text('zzzz\n')
        second = Momblish.english()

        assert first.corpus == second.corpus

    def test_rebuilds_cached_english_corpus(self, monkeypatch, tmp_path):
        """Rebuilds the cached english corpus when requested"""

        dict_file = tmp_path / 'words'
        dict_file.write_text('\n'.join(test_corpus))
        monkeypatch.setattr('momblish.momblish.lookup_dict', lambda lang: str(dict_file))
        monkeypatch.setenv('XDG_CACHE_HOME', str(tmp_path / 'cache'))

        first = Momblish.english()

        dict_file.write_text('abce\nabcf\n')
        rebuilt = Momblish.english(rebuild_cache=True)

        assert first.corpus != rebuilt.corpus

    def test_caches_custom_corpus_file(self, monkeypatch, tmp_path):
        """Caches an analyzed user-provided corpus file"""

        corpus_file = tmp_path / 'custom.txt'
        corpus_file.write_text('\n'.join(test_corpus))
        monkeypatch.setenv('XDG_CACHE_HOME', str(tmp_path / 'cache'))

        first = Momblish.from_file(str(corpus_file))

        cache_files = list((tmp_path / 'cache' / 'momblish').glob('corpus-*.json'))
        assert len(cache_files) == 1

        corpus_file.write_text('zzzz\n')
        second = Momblish.from_file(str(corpus_file))

        assert first.corpus == second.corpus

    def test_rebuilds_cached_custom_corpus_file(self, monkeypatch, tmp_path):
        """Rebuilds a cached user-provided corpus file when requested"""

        corpus_file = tmp_path / 'custom.txt'
        corpus_file.write_text('\n'.join(test_corpus))
        monkeypatch.setenv('XDG_CACHE_HOME', str(tmp_path / 'cache'))

        first = Momblish.from_file(str(corpus_file))

        corpus_file.write_text('abce\nabcf\n')
        rebuilt = Momblish.from_file(str(corpus_file), rebuild_cache=True)

        assert first.corpus != rebuilt.corpus
