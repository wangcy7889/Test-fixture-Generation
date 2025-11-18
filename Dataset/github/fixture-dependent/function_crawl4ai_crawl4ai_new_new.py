import re
from typing import List
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def preprocess_text(self, text: str) -> List[str]:
    parts = [x.strip() for x in text.split('|')] if '|' in text else [text]
    parts[0] = re.sub('^(.*?):', '\\1', parts[0])
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english')) - {'how', 'what', 'when', 'where', 'why', 'which'}
    tokens = []
    for part in parts:
        if '(' in part and ')' in part:
            code_tokens = re.findall('[\\w_]+(?=\\()|[\\w_]+(?==[\\\'"]{1}[\\w_]+[\\\'"]{1})', part)
            tokens.extend(code_tokens)
        words = word_tokenize(part.lower())
        tokens.extend([lemmatizer.lemmatize(token) for token in words if token not in stop_words])
    return tokens