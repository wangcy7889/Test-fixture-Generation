import nltk

def f_chartparser(sentence):
    grammar = nltk.CFG.fromstring("""
        S -> NP VP
        NP -> Det N
        VP -> V NP
        Det -> 'the'
        N -> 'dog' | 'cat'
        V -> 'chased'
    """)
    parser = nltk.ChartParser(grammar)
    return list(parser.parse(sentence.split()))