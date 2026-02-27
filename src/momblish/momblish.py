from momblish.corpus_analyzer import CorpusAnalyzer
from momblish.corpus import Corpus

from itertools import count as _count
import hashlib
import random
import os


DICT = {
    'english': ['/usr/share/dict/words', '/usr/dict/words', '/usr/share/dict/web2']
}


def lookup_dict(lang):
    for location in DICT[lang]:
        if os.path.exists(location):
            return location


def cache_home():
    xdg_cache_home = os.environ.get('XDG_CACHE_HOME')
    if xdg_cache_home and os.path.isabs(xdg_cache_home):
        return xdg_cache_home

    return os.path.join(os.path.expanduser('~'), '.cache')


def cache_path(name):
    directory = os.path.join(cache_home(), 'momblish')
    os.makedirs(directory, mode=0o700, exist_ok=True)
    return os.path.join(directory, '{0}.json'.format(name))


def corpus_cache_name(path):
    digest = hashlib.sha256(os.path.abspath(path).encode('utf-8')).hexdigest()
    return 'corpus-{0}'.format(digest)


class EmptyCorpusError(Exception):
    """You have to analzye a corpus to generate words"""
    def __init__(self, message):
        self.message = message


class Momblish(object):
    def __init__(self, corpus=None):
        self.corpus = corpus if corpus else Corpus()

        if not (corpus.weighted_bigrams and corpus.occurrences):
            raise EmptyCorpusError('Your corpus has no words')

    @classmethod
    def english(cls, rebuild_cache=False):
        return cls.load_analyzed_corpus(
            lookup_dict('english'),
            cache_name='english',
            rebuild_cache=rebuild_cache,
        )

    @classmethod
    def from_file(cls, path, rebuild_cache=False):
        return cls.load_analyzed_corpus(
            path,
            cache_name=corpus_cache_name(path),
            rebuild_cache=rebuild_cache,
        )

    @classmethod
    def load_analyzed_corpus(cls, path, cache_name, rebuild_cache=False):
        analyzed_corpus_path = cache_path(cache_name)
        if os.path.exists(analyzed_corpus_path) and not rebuild_cache:
            return cls(Corpus.load(analyzed_corpus_path))

        with open(path, 'r') as corpus_file:
            corpus = CorpusAnalyzer(corpus_file).corpus
        corpus.save(analyzed_corpus_path)
        return cls(corpus)

    def random_starting_bigram(self, prefix=None):
        bigrams = [
            bigram for bigram in self.corpus.weighted_bigrams
            if prefix is None or bigram.startswith(prefix)
        ]

        if not bigrams:
            raise ValueError('Your prefix has no matching words in the corpus')

        weights = [self.corpus.weighted_bigrams[bigram] for bigram in bigrams]
        return random.choices(bigrams, weights=weights)[0]

    def resolve_length(self, length, prefix):
        if length is not None:
            if prefix and len(prefix) > length:
                raise ValueError('Your prefix is longer than the requested word length')
            return length

        min_length = max(4, len(prefix) if prefix else 0)
        return random.randint(min_length, max(min_length, 10))

    def validate_prefix(self, prefix):
        if len(prefix) == 1:
            if not any(bigram.startswith(prefix) for bigram in self.corpus.weighted_bigrams):
                raise ValueError('Your prefix has no matching words in the corpus')
            return

        if prefix[0:2] not in self.corpus.weighted_bigrams:
            raise ValueError('Your prefix has no matching words in the corpus')

        for index in range(2, len(prefix)):
            bigram = prefix[index - 2:index]
            next_letter = prefix[index]
            if next_letter not in self.corpus.occurrences[bigram]:
                raise ValueError('Your prefix has no matching words in the corpus')

    def starting_word(self, prefix, length):
        if not prefix:
            return self.random_starting_bigram()

        prefix = prefix.upper()
        self.validate_prefix(prefix)

        if len(prefix) == 1 and length > 1:
            return self.random_starting_bigram(prefix=prefix)

        return prefix

    def word(self, length=None, prefix=None):
        length = self.resolve_length(length, prefix)
        word = self.starting_word(prefix, length)

        for _ in range(length - len(word)):
            last_bigram = word[-2:]
            next_letter = random.choices(
                    list(self.corpus.occurrences[last_bigram]),
                    weights=self.corpus.occurrences[last_bigram].values())[0]
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
