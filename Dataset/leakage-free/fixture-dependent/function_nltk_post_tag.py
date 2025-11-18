from nltk.tokenize import word_tokenize
from nltk import pos_tag


def pos_tag_file_with_nltk(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        tokens = word_tokenize(text)
        tagged_words = pos_tag(tokens)
        return tagged_words
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise e
