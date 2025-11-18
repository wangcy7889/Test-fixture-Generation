from nltk.tokenize import sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer


def analyze_sentiment(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        sentences = sent_tokenize(text)
        sid = SentimentIntensityAnalyzer()

        sentiment_results = []
        for sentence in sentences:
            sentiment_results.append(sid.polarity_scores(sentence))

        return sentiment_results

    except FileNotFoundError as e:
        raise FileNotFoundError(e)
    except Exception as e:
        raise Exception(e)