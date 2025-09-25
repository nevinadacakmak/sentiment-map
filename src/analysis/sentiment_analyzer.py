from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


class SentimentAnalyzer:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text: str) -> dict:
        if not isinstance(text, str):
            text = ''
        return self.sid.polarity_scores(text)

    def analyze_sentiments_in_dataframe(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        # Apply sentiment analysis and expand scores into columns
        df = df.copy()
        df['sentiment_scores'] = df[text_column].apply(self.analyze_sentiment)
        df['neg'] = df['sentiment_scores'].apply(lambda x: x.get('neg', 0.0))
        df['neu'] = df['sentiment_scores'].apply(lambda x: x.get('neu', 0.0))
        df['pos'] = df['sentiment_scores'].apply(lambda x: x.get('pos', 0.0))
        df['compound'] = df['sentiment_scores'].apply(lambda x: x.get('compound', 0.0))
        df['sentiment'] = df['compound'].apply(self.categorize_sentiment)
        return df

    @staticmethod
    def categorize_sentiment(compound_score: float) -> str:
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'