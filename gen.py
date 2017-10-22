#!/usr/bin/env python

from chain import MarkovChain

_long_words = lambda k: max(len(k) - 2, 1)
_heavily_bias = lambda k: 100


if __name__ == '__main__':
    mc = MarkovChain()
    mc.ingest_from_file('training_set.txt', E=_long_words)  # Ex: Bias for long words in corpus `training_set.txt`
    mc.ingest_from_file('hbisms.txt', E=_heavily_bias)  # Yeah, no idea.
    mc.save('training.json')
    print ''.join(w for w in mc(max_length=100))
