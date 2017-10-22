#!/usr/bin/env python

from chain import MarkovChain

_long_words = lambda w1, w2: max(len(w2) - 5, 1)
_alternating = lambda w1, w2: max(abs(len(w1)-len(w2)), 1)
_heavily_bias = lambda w1, w2: 100


if __name__ == '__main__':
    mc = MarkovChain()
    mc.ingest_from_file('training_set.txt', E=_alternating)  # Ex: Bias for long words in corpus `training_set.txt`
    mc.ingest_from_file('hbisms.txt', E=_heavily_bias)  # Yeah, no idea.
    mc.save('training.json')
    print ''.join(w for w in mc(max_length=100))
