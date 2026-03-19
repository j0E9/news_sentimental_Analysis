from textblob import TextBlob

def get_sentiment(text):
    if not text:
        return 0

    analysis = TextBlob(text)
    return analysis.sentiment.polarity