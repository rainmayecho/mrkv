#!/usr/bin/env python

from chain import MarkovChain
from train import (
    long_words,
    prefer_punctuation,
    standard,
    TrainingFunction
)

# Mostly useless, we can just retrain after the tree is built.
_long_words = lambda w1, w2: max(len(w2) - 5, 1)
_alternating = lambda w1, w2: max(abs(len(w1)-len(w2)), 1)
_heavily_bias = lambda w1, w2: 25

train = True

if __name__ == '__main__':
    mc = MarkovChain()
    if train:
        mc.ingest_from_file('training_set.txt')
        mc.ingest_from_file('training_set_2.txt')
        mc.ingest_from_file('hbisms.txt', E=_heavily_bias)  # Yeah, no idea.
        F = TrainingFunction([(prefer_punctuation, 1), (long_words, 1), (standard, .5)])  # Care about punctuation N times as much as having long words.
        mc.train(F=F)
        mc.save('training.json')
    else:
        mc.load('training.json')
    print ''.join(w for w in mc(max_length=100))
