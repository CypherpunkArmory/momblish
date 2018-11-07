import json


class Corpus(object):
    def __init__(self, weighted_bigrams={}, occurences={}):
        self.weighted_bigrams = weighted_bigrams
        self.occurences = occurences

    @classmethod
    def load(cls, path):
        with open(path, 'r') as f:
            data = f.read()

        return cls(**json.loads(data))

    def __eq__(self, other):
        return self.weighted_bigrams == other.weighted_bigrams and self.occurences == other.occurences

    def save(self, path):
        saved_corpus = {
            'weighted_bigrams': self.weighted_bigrams,
            'occurences': self.occurences
        }

        with open(path, 'w') as f:
            f.write(json.dumps(saved_corpus))
