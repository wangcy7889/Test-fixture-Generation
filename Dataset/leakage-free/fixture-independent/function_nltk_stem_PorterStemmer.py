from nltk.stem import PorterStemmer


def f_stem(word):
    porter_stemmer = PorterStemmer()
    return porter_stemmer.stem(word)