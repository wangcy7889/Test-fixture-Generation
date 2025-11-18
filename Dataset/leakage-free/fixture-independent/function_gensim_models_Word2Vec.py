from gensim.models import Word2Vec

def train_word2vec_model(sentences):
    
    model = Word2Vec(sentences, vector_size=50, window=3, min_count=1, workers=4)
    return model
