from itertools import groupby, chain
from collections import defaultdict
from momblish.corpus import Corpus
import string


def each_cons(xs, n):
    return zip(*(xs[i:] for i in range(n)))


class CorpusAnalyzer(object):
    def __init__(self, corpus=()):
        self.words = [word.rstrip() for word in corpus]
        self.corpus = Corpus({}, {})
        self.init_weighted_bigrams()
        self.init_occurrences()

    def init_weighted_bigrams(self):
        starting_bigrams = {}

        def filtered_words():
            for word in self.words:
                if len(word) > 2 and string.punctuation not in word[0:2]:
                    yield word

        # FIXME Counter would work here but doesn't do normalized distro
        # split each word into a set of "bigrams" (sets of 2 letters)
        for word in filtered_words():
            bigram = word[0:2].upper()

            if bigram in starting_bigrams:
                starting_bigrams[bigram] += 1
            else:
                starting_bigrams[bigram] = 1

        # we sum the total number of OCCURRENCES of each bigram to give us a
        # weighted average of the chances that a word starts with particular
        # bigram
        # common bigram:  TH
        # uncommon bigram: ZX
        total = sum(starting_bigrams.values())

        for bigram, count in starting_bigrams.items():
            # assign all of the known bigrams a weight given their frequency
            self.corpus.weighted_bigrams[bigram] = count / total

    def init_occurrences(self):
        # assemble a list of trigrams in all the worlds
        punct_and_newline = set(string.punctuation + "\n")
        trigrams = []
        for word in self.words:
            if punct_and_newline.isdisjoint(set(word)):
                trigrams.append(list(each_cons(word.upper(), 3)))

        # flatten to a global list of trigrams
        trigrams = list(chain.from_iterable(trigrams))

        # FIXME Counter would work here but doesn't do normalized distro
        # group the trigrams by their beginning bigram
        # and store the frequency of the last letter into the occurrence hash
        self.corpus.occurrences = defaultdict(dict)
        for bigram, trigram in groupby(trigrams, lambda x: ''.join(x[0:2])):
            last_char = list(trigram)[0][-1]

            if last_char in self.corpus.occurrences[bigram]:
                self.corpus.occurrences[bigram][last_char] += 1
            else:
                self.corpus.occurrences[bigram][last_char] = 1

        # convert that raw occurrence numbers into relative frequency
        for bigram, last_letters in self.corpus.occurrences.items():
            total = sum(last_letters.values())
            for last_letter in last_letters:
                self.corpus.occurrences[bigram][last_letter] /= total
