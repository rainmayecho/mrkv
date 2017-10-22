
def standard(w1, w2):
    return 1

def long_words(w1, w2):
    return max(len(w1 + w2), 12) / 12.0

def alternating_long_words(w1, w2):
    return min(abs(len(w1) - len(w2)), 4) / 4.0

def prefer_punctuation(w1, w2):
    return int(w2[-1] in '.!?' or w1[-1] in '.!?')

def translate_result(r):
    return (r - 0.5) * 2


class TrainingFunction(object):
    """
    Takes a list of (function, weight) tuples to build a single
    function F(w1, w2) representing a score between [-1, 1].
    """
    def __init__(self, *wfns):
        self.components, = wfns
        self.func = self.build_fn()

    def build_fn(self):
        def wrap(w1, w2):
            v = [weight * translate_result(fn(w1, w2)) for (fn, weight) in self.components]  # [ score per fn ]
            mag_v = sum(vi**2 for vi in v)**.5  # magnitude of the vector? ex: [-3, 4] => 5
            r = sum(vi/float(mag_v) for vi in v)  # -3/5 + 4/5 = 0.2 => slightly increase the importance of this edge!
            return r
        return wrap

    def __str__(self):
        return ' + '.join('(%s * %s)' % (w, f.__name__) for f, w in self.components)

    def __call__(self, w1, w2):
        return self.func(w1, w2)
