from momblish.corpus_analyzer import CorpusAnalyzer
from momblish.corpus import Corpus

from itertools import count as _count
import random
import os


DICT = {
    'english': ['/usr/share/dict/words', '/usr/dict/words', '/usr/share/dict/web2']
}


def lookup_dict(lang):
    for location in DICT[lang]:
        if os.path.exists(location):
            return location


class EmptyCorpusError(Exception):
    """You have to analzye a corpus to generate words"""
    def __init__(self, message):
        self.message = message


class Momblish(object):
    def __init__(self, corpus=None):
        self.corpus = corpus if corpus else Corpus()

        if not (corpus.weighted_bigrams and corpus.occurences):
            raise EmptyCorpusError('Your corpus has no words')

    @classmethod
    def english(cls):
        dict_file = lookup_dict('english')
        corpus = CorpusAnalyzer(open(dict_file, 'r')).corpus
        return cls(corpus)

    def word(self, length=None):
        length = length if length else random.randint(4, 10)

        word = random.choices(
                list(self.corpus.weighted_bigrams.keys()),
                weights=self.corpus.weighted_bigrams.values())[0]

        for _ in range(length-2):
            last_bigram = word[-2:]
            next_letter = random.choices(
                    list(self.corpus.occurences[last_bigram]),
                    weights=self.corpus.occurences[last_bigram].values())[0]
            word += next_letter

        return word

    def sentence(self, count=None, word_length=None):
        def counter():
            if count:
                for n in range(count):
                    yield n
            else:
                for n in _count():
                    yield n

        for _ in counter():
            yield self.word(length=word_length)
