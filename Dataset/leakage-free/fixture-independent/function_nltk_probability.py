import nltk
from nltk.probability import FreqDist, MLEProbDist


def f_probability(text):
    fd = FreqDist(text)
    return MLEProbDist(fd)