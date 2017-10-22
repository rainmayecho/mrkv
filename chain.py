
import io
import json
import random
import re

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

DEFAULT_RAND_FN = lambda k: random.random() * k
DEFAULT_EVALUATION_FN = lambda w: 1

class MarkovChain(object):
    RAND_FN = lambda x: random.random() * x

    def __init__(self):
        self.tree = {}

    def ingest(self, corpus, E=DEFAULT_EVALUATION_FN):
        words = filter(bool, re.split(r'[\s+]', corpus))
        words = [word.lower() for word in words]
        for w1, w2 in [(words[i], words[i+1]) for i in xrange(len(words) - 1)]:
            if w1 not in self.tree:
                self.tree[w1] = {}
            if w2 not in self.tree[w1]:
                self.tree[w1][w2] = E(w1, w2)
            else:
                self.tree[w1][w2] += E(w1, w2)
        return True

    def ingest_from_file(self, filename, **kwargs):
        try:
            with open(filename, 'r') as f:
                return self.ingest(f.read(), **kwargs)
        except UnicodeDecodeError:
            print 'Unable to decode'
        return False

    def _load_tree(self, filename):
        with open(filename, 'r') as f:
            self.tree = json.load(f)

    def _save_tree(self, filename):
        with io.open(filename, 'w', encoding='utf-8') as f:
            s = json.dumps(self.tree,
                           indent=4,
                           sort_keys=True,
                           separators=(',', ': '),
                           ensure_ascii=False)
            f.write(to_unicode(s))

    def load(self, filename):
        self._load_tree(filename)

    def save(self, filename):
        self._save_tree(filename)

    def _generate_text(self, max_length=0, randomize=DEFAULT_RAND_FN):
        if not len(self.tree):
            return

        word = random.choice([k for k in self.tree])
        yield word
        i = 1
        while i < max_length:
            i += 1
            if word not in self.tree:
                return
            _next = sorted([(w, randomize(self.tree[word][w] / float(len(self.tree[word])))) for w in self.tree[word]], key=lambda k: 1 - k[1])
            word = _next[0][0]
            yield word

    def generate_text(self, *args, **kwargs):

        def should_capitalize(lc):
            return lc in '.!?"'

        lc = '.'
        for w in self._generate_text(*args, **kwargs):
            s = w.capitalize() if should_capitalize(lc) else w[0] + w[1:].capitalize() if should_capitalize(w[0]) else w
            s += ' '
            yield s
            lc = s[-2]

    def __call__(self, *args, **kwargs):
        return self.generate_text(*args, **kwargs)
