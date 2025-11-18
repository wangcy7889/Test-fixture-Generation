from gensim.models import KeyedVectors

def find_most_similar_words(model, word, topn=5):
    
    try:
        similar_words = model.most_similar(word, topn=topn)
        return similar_words
    except KeyError:
        raise ValueError(f"Error: word '{word}' Not found in the word vector model.")
