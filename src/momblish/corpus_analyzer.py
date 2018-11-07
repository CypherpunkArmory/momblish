from itertools import groupby, chain
from momblish.corpus import Corpus
import string


def each_cons(xs, n):
    return zip(*(xs[i:] for i in range(n)))


class CorpusAnalyzer(object):
    def __init__(self, corpus=iter([])):
        self.words = [word.rstrip() for word in corpus]
        self.corpus = Corpus({}, {})
        self.init_weighted_bigrams()
        self.init_occurences()

    def init_weighted_bigrams(self):
        starting_bigrams = {}

        # FIXME Counter would work here but doesn't do normalized distro
        # split each word into a set of "bigrams" (sets of 2 letters)
        for word in self.words:
            bigram = word[0:2].upper()

            if len(bigram) < 2 or string.punctuation in bigram:
                continue

            if bigram in starting_bigrams:
                starting_bigrams[bigram] += 1
            else:
                starting_bigrams[bigram] = 1

        # we sum the total number of OCCURENCES of each bigram to give us a
        # weighted average of the chances that a word starts with particular
        # bigram
        # common bigram:  TH
        # uncommon bigram: ZX
        total = sum(starting_bigrams.values())

        for bigram, count in starting_bigrams.items():
            # assign all of the known bigrams a weight given their frequency
            self.corpus.weighted_bigrams[bigram] = count / total

    def init_occurences(self):
        # assemble a list of trigrams in all the worlds
        trigrams = []
        for word in self.words:
            if set(string.punctuation + "\n").isdisjoint(set(word)):
                trigrams.append(list(each_cons(word.upper(), 3)))

        # flatten to a global list of trigrams
        trigrams = list(chain.from_iterable(trigrams))

        # FIXME Counter would work here but doesn't do normalized distro
        # group the trigrams by their beginning bigram
        # and store the frequency of the last letter into the occurence hash
        self.corpus.occurences = {}
        for bigram, trigram in groupby(trigrams, lambda x: ''.join(x[0:2])):
            if bigram not in self.corpus.occurences:
                self.corpus.occurences[bigram] = {}

            last_char = list(trigram)[0][-1]

            if last_char in self.corpus.occurences[bigram]:
                self.corpus.occurences[bigram][last_char] += 1
            else:
                self.corpus.occurences[bigram][last_char] = 1

        # convert that raw occurence numbers into relative frequency
        for bigram, last_letters in self.corpus.occurences.items():
            total = sum(last_letters.values())
            for last_letter in last_letters:
                self.corpus.occurences[bigram][last_letter] /= total
