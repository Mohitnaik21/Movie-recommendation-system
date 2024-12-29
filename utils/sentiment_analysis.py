from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiments(reviews):
    sia = SentimentIntensityAnalyzer()
    sentiments = []
    for review in reviews:
        sentiment = sia.polarity_scores(review['content'])
        sentiments.append({
            'author': review['author'],
            'content': review['content'],
            'sentiment': sentiment
        })
    return sentiments

def highlight_positive_reviews(sentiments):
    return [r for r in sentiments if r['sentiment']['compound'] > 0.05]
